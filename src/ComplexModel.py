import pandas as pd
from collections import deque
from typing import Any, List, Dict
from sklearn.metrics import mean_squared_error
from CONST import *


class ComplexModel():
    def __init__(self,
                 alpha_w: float,
                 Idry: float,
                 Iwet: float,
                 Emax: float,
                 perc_rate: float,
                 lag_q: int,
                 lag_b: int,
                 w_q: float,
                 w_b: float,
                 w_t: float,
                 capacity_clay: float,
                 capacity_gravel: float,
                 capacity_organic: float,
                 capacity_sand_coarse: float,
                 capacity_sand_fine: float,
                 capacity_sand_medium: float,
                 capacity_silt: float,
                 capacity_urban: float,
                 capacity_stone: float,
                 w_wetness_percipitation: float,
                 w_wetness_soilstore: float,
                 location: str,
                 Scf: float = 50.0,  # Field capacity threshold
                 Gmax: float = 500.0,  # Maximum groundwater depth
                 gw_init: float = 250.0,  # Initial groundwater depth
                 gw_recharge_factor: float = 0.1,  # How percolation affects GW depth
                 gw_drain_factor: float = 0.05,  # How baseflow affects GW depth
                 ) -> None:
        """
        Additional parameters compared to SimpleModel:
        capacity_*: Storage capacity for each soil type
        w_wetness_percipitation: Weight for precipitation in wetness calculation
        w_wetness_soilstore: Weight for soil store in wetness calculation
        location: Location name to look up soil percentages
        Scf: Soil level above which percolation occurs
        Gmax: Maximum groundwater depth
        gw_init: Initial groundwater depth
        gw_recharge_factor: Weight controlling how percolation reduces GW depth
        gw_drain_factor: Weight controlling how baseflow increases GW depth
        """
        # Parameters
        self.alpha_w = alpha_w
        self.Idry = Idry
        self.Iwet = Iwet
        self.Emax = Emax
        self.perc_rate = perc_rate
        self.w_q = w_q
        self.w_b = w_b
        self.w_t = w_t

        # States
        self.wetness = 0.0
        self.soil = 0.0
        self.groundwater = gw_init

        # Routing stores
        self.quick_queue = deque([0.0] * lag_q)
        self.base_queue = deque([0.0] * lag_b)

        # Outputs
        self.Q = 0.0

        # Soil type capacities
        self.capacity_clay = capacity_clay
        self.capacity_gravel = capacity_gravel
        self.capacity_organic = capacity_organic
        self.capacity_sand_coarse = capacity_sand_coarse
        self.capacity_sand_fine = capacity_sand_fine
        self.capacity_sand_medium = capacity_sand_medium
        self.capacity_silt = capacity_silt
        self.capacity_urban = capacity_urban
        self.capacity_stone = capacity_stone

        # Wetness weights
        self.w_wetness_percipitation = w_wetness_percipitation
        self.w_wetness_soilstore = w_wetness_soilstore

        # Groundwater parameters
        self.Scf = Scf
        self.Gmax = Gmax
        self.gw_recharge_factor = gw_recharge_factor
        self.gw_drain_factor = gw_drain_factor

        # Calculate location Smax from perentages of soil type
        self.Smax = (self.capacity_clay * SOIL_PERCENTAGES[location]["clay"] +
                     self.capacity_gravel * SOIL_PERCENTAGES[location]["gravel"] +
                     self.capacity_organic * SOIL_PERCENTAGES[location]["organic"] +
                     self.capacity_sand_coarse * SOIL_PERCENTAGES[location]["sand_coarse"] +
                     self.capacity_sand_fine * SOIL_PERCENTAGES[location]["sand_fine"] +
                     self.capacity_sand_medium * SOIL_PERCENTAGES[location]["sand_medium"] +
                     self.capacity_silt * SOIL_PERCENTAGES[location]["silt"] +
                     self.capacity_urban * SOIL_PERCENTAGES[location]["urban"] +
                     self.capacity_stone * SOIL_PERCENTAGES[location]["stone"]
                     )

    def step(self, Pt, PET, Qt_minus_1=0.0) -> dict[str, Any]:
        """
        One daily timestep with additional complexity:
        """

        # Wetness update (complex: includes soil store)
        self.wetness = (self.alpha_w * self.wetness +
                        self.w_wetness_percipitation * Pt +
                        self.w_wetness_soilstore * self.soil)
        wt = min(self.wetness / self.Idry, 1.0)

        # Infiltration capacity
        Icap = self.Idry * (1 - wt) + self.Iwet * wt
        Pin = min(Pt, Icap)
        Pq = Pt - Pin

        # Soil store
        self.soil += Pin
        self.soil = min(self.soil, self.Smax)

        # Evaporation
        Et = min(PET, self.Emax * (self.soil / self.Smax))  # Actual ET
        self.soil -= Et  # Remove evaporated water

        # Percolation with groundwater influence
        if self.groundwater < self.Gmax:
            gw_factor = 1 - (self.groundwater / self.Gmax)
        else:
            gw_factor = 0.0

        perc = self.perc_rate * max(0.0, self.soil - self.Scf) * gw_factor
        self.soil -= perc
        Qb = perc

        # Update groundwater depth
        self.groundwater = self.groundwater - self.gw_recharge_factor * perc + self.gw_drain_factor * Qb
        self.groundwater = max(0.0, min(self.groundwater, self.Gmax))

        # Quick flow
        Qq = Pq  # Surface runoff

        # Routing
        self.quick_queue.append(Qq)
        routed_q = self.quick_queue.popleft()

        self.base_queue.append(Qb)
        routed_b = self.base_queue.popleft()

        # Discharge
        self.Q = (
                self.w_q * routed_q +  # Weighted routed quick flow
                self.w_b * routed_b +  # Weighted routed baseflow
                self.w_t * Qt_minus_1  # Weighted previous discharge
        )

        return {
            "Q": self.Q,
            "Qq": routed_q,
            "Qb": routed_b,
            "soil": self.soil,
            "wetness": wt,
            "Et": Et,
            "groundwater": self.groundwater,
            "percolation": perc
        }

    def run_dataframe(
            self,
            df: pd.DataFrame,
            pt_col: str,
            pet_col: str,
            q0: float = 0.0
    ) -> List[Dict[str, float]]:
        """
        Run the model over a dataframe
        """
        results: List[Dict[str, float]] = []
        Qt_prev = q0

        for _, row in df.iterrows():
            Pt = float(row[pt_col])
            PET = float(row[pet_col])

            out = self.step(Pt=Pt, PET=PET, Qt_minus_1=Qt_prev)
            results.append(out)

            Qt_prev = float(row['ALFANUMERIEKEWAARDE'])

        return results

    def score(self, df, target, q_col="Q", n=31, pt_col="RD", pet_col="EV24", q0=0.0):
        """
        Calculate MSE score for model predictions
        """
        results = self.run_dataframe(df=df, pt_col=pt_col, pet_col=pet_col, q0=q0)
        results_df = pd.DataFrame(results)
        return mean_squared_error(target[:n], results_df[q_col][:n])
