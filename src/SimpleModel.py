from collections import deque
from typing import Any, List, Dict
import pandas as pd
from sklearn.metrics import mean_squared_error


class SimpleModel:
    def __init__(self,
                 alpha_w: float,
                 Idry: float,
                 Iwet: float,
                 Smax: float,
                 Emax: float,
                 perc_rate: float,
                 lag_q: int,
                 lag_b: int,
                 w_q: float,
                 w_b: float,
                 w_t: float,
                 ) -> None:
        """
        alpha_w: Higher values imply slower drying of the catchment and longer memory of past rainfall.
        Idry: Represents how much precipitation can infiltrate when the soil is dry.
        Iwet: Maximum infiltration capacity (mm/day) under fully saturated soil conditions.
        Smax: Represents the amount of water that can be held in the soil layer between the surface and the
            groundwater.
        Emax: Maximum evapotranspiration rate (mm/day) from the soil store.
        perc_rate: Percolation rate coefficient.
        lag_q: Routing lag (days) for quick flow (surface runoff).
        lag_b: Routing lag (days) for baseflow (groundwater discharge).
        w_q :Weighting factor (-) for the contribution of routed quick flow to total discharge.
        w_b: Weighting factor (-) for the contribution of routed baseflow to total discharge.
        """

        # Parameters
        self.alpha_w = alpha_w
        self.Idry = Idry
        self.Iwet = Iwet
        self.Smax = Smax
        self.Emax = Emax
        self.perc_rate = perc_rate
        self.w_q = w_q
        self.w_b = w_b
        self.w_t = w_t

        # States
        self.wetness = 0.0
        self.soil = 0.0

        # Routing stores
        self.quick_queue = deque([0.0] * lag_q)
        self.base_queue = deque([0.0] * lag_b)

        # Outputs
        self.Q = 0.0

    def step(self, Pt, PET, Qt_minus_1=0.0) -> dict [str, Any]:
        """
        One daily timestep
        """

        # --- Wetness update ---
        self.wetness = self.alpha_w * self.wetness + (1 - self.alpha_w) * Pt
        wt = min(self.wetness / self.Idry, 1.0)

        # --- Infiltration capacity ---
        Icap = self.Idry * (1 - wt) + self.Iwet * wt
        Pin = min(Pt, Icap)
        Pq = Pt - Pin

        # --- Soil store ---
        self.soil += Pin
        self.soil = min(self.soil, self.Smax)

        # --- Evaporation ---
        Et = min(PET, self.Emax * (self.soil / self.Smax))
        self.soil -= Et

        # --- Percolation ---
        perc = self.perc_rate * wt * self.soil
        self.soil -= perc
        Qb = perc

        # --- Quick flow ---
        Qq = Pq  # 100% routed for now

        # --- Routing ---
        self.quick_queue.append(Qq)
        routed_q = self.quick_queue.popleft()

        self.base_queue.append(Qb)
        routed_b = self.base_queue.popleft()

        # --- Discharge ---
        self.Q = (
            self.w_q * routed_q +
            self.w_b * routed_b +
            self.w_t * Qt_minus_1
        )

        return {
            "Q": self.Q,
            "Qq": routed_q,
            "Qb": routed_b,
            "soil": self.soil,
            "wetness": wt,
            "Et": Et
        }

    def run_dataframe(
        self,
        df: pd.DataFrame,
        pt_col: str,
        pet_col: str,
        q0: float = 0.0
    ) -> List[Dict[str, float]]:
        """
        Run the model
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

    def score(model, df, target, q_col="Q", n=31, pt_col="RD", pet_col="EV24", q0=0.0):
        results = model.run_dataframe(df=df, pt_col=pt_col, pet_col=pet_col, q0=q0)
        results_df = pd.DataFrame(results)
        return mean_squared_error(target[:n], results_df[q_col][:n])
