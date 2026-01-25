SIMPLE_MODEL_PARAM_NAMES = [
    "alpha_w", "Idry", "Iwet", "Smax", "Emax", "perc_rate", "lag_q", "lag_b", "w_q", "w_b", "w_t"
]
SIMPLE_MODEL_PARAM_RANGES = {
    "alpha_w": (0.0, 1.0),
    "Idry": (1.0, 500.0),
    "Iwet": (1.0, 100.0),
    "Smax": (1.0, 1200.0),
    "Emax": (1.0, 10.0),
    "perc_rate": (0.001, 0.99),
    "lag_q": (0, 10),
    "lag_b": (10, 20),
    "w_q": (1.0, 1000.0),
    "w_b": (1.0, 1000.0),
    "w_t": (0.0, 1.0)
}
SIMPLE_MODEL_PARAM_STEPS = {
    "alpha_w": 0.05,
    "Idry": 10.0,
    "Iwet": 2.0,
    "Smax": 50.0,
    "Emax": 0.5,
    "perc_rate": 0.001,
    "lag_q": 1,
    "lag_b": 1,
    "w_q": 1,
    "w_b": 1,
    "w_t": 0.05
}
SIMPLE_MODEL_INITIAL_PARAMS = {
    "alpha_w": 0.5,
    "Idry": 250.0,
    "Iwet": 50.0,
    "Smax": 600.0,
    "Emax": 5.0,
    "perc_rate": 0.01,
    "lag_q": 5,
    "lag_b": 15,
    "w_q": 1,
    "w_b": 1,
    "w_t": 0.5
}

COMPLEX_MODEL_PARAM_NAMES = [
    "alpha_w", "Idry", "Iwet", "Emax", "perc_rate", "lag_q", "lag_b", "w_q", "w_b", "w_t",
    "capacity_clay", "capacity_gravel", "capacity_organic", "capacity_sand_coarse",
    "capacity_sand_fine", "capacity_sand_medium", "capacity_silt", "capacity_urban", "capacity_stone",
    "w_wetness_percipitation", "w_wetness_soilstore", "Scf", "Gmax", "gw_init",
    "gw_recharge_factor", "gw_drain_factor"
]

# Parameter ranges for calibration
COMPLEX_MODEL_PARAM_RANGES = {
    "alpha_w": (0.0, 1.0),
    "Idry": (1.0, 500.0),
    "Iwet": (1.0, 100.0),
    "Emax": (1.0, 10.0),
    "perc_rate": (0.001, 0.1),
    "lag_q": (0, 10),
    "lag_b": (10, 30),
    "w_q": (1.0, 10000.0),
    "w_b": (1.0, 10000.0),
    "w_t": (0.0, 1.0),
    "capacity_clay": (10.0, 500.0),
    "capacity_gravel": (10.0, 500.0),
    "capacity_organic": (10.0, 500.0),
    "capacity_sand_coarse": (10.0, 500.0),
    "capacity_sand_fine": (10.0, 500.0),
    "capacity_sand_medium": (10.0, 500.0),
    "capacity_silt": (10.0, 500.0),
    "capacity_urban": (10.0, 500.0),
    "capacity_stone": (10.0, 500.0),
    "w_wetness_percipitation": (0.0, 1.0),
    "w_wetness_soilstore": (0.0, 1.0),
    "Scf": (10.0, 500.0),
    "Gmax": (100.0, 1000.0),
    "gw_init": (0.0, 1000.0),
    "gw_recharge_factor": (0.01, 0.5),
    "gw_drain_factor": (0.01, 0.5)
}
COMPLEX_MODEL_INITIAL_PARAMS = {
    "alpha_w": 0.5,
    "Idry": 250.0,
    "Iwet": 50.0,
    "Emax": 5.0,
    "perc_rate": 0.01,
    "lag_q": 5,
    "lag_b": 15,
    "w_q": 1.0,
    "w_b": 1.0,
    "w_t": 0.5,
    "capacity_clay": 100.0,
    "capacity_gravel": 100.0,
    "capacity_organic": 100.0,
    "capacity_sand_coarse": 100.0,
    "capacity_sand_fine": 100.0,
    "capacity_sand_medium": 100.0,
    "capacity_silt": 100.0,
    "capacity_urban": 100.0,
    "capacity_stone": 100.0,
    "w_wetness_percipitation": 0.5,
    "w_wetness_soilstore": 0.5,
    "Scf": 50.0,
    "Gmax": 500.0,
    "gw_init": 250.0,
    "gw_recharge_factor": 0.1,
    "gw_drain_factor": 0.05
}

COMPLEX_MODEL_PARAM_STEPS = {
    "alpha_w": 0.05,
    "Idry": 10.0,
    "Iwet": 2.0,
    "Emax": 0.5,
    "perc_rate": 0.001,
    "lag_q": 1,
    "lag_b": 1,
    "w_q": 1,
    "w_b": 1,
    "w_t": 0.05,
    "capacity_clay": 10.0,
    "capacity_gravel": 10.0,
    "capacity_organic": 10.0,
    "capacity_sand_coarse": 10.0,
    "capacity_sand_fine": 10.0,
    "capacity_sand_medium": 10.0,
    "capacity_silt": 10.0,
    "capacity_urban": 10.0,
    "capacity_stone": 10.0,
    "w_wetness_percipitation": 0.05,
    "w_wetness_soilstore": 0.05,
    "Scf": 10.0,
    "Gmax": 50.0,
    "gw_init": 50.0,
    "gw_recharge_factor": 0.01,
    "gw_drain_factor": 0.01
}

# --- COMPLEX_MODEL_V2 variables (for ComplexModel_V2 only) ---
COMPLEX_MODEL_V2_PARAM_NAMES = [
    "alpha_w", "Idry", "Iwet", "Emax", "perc_rate", "lag_q", "lag_b", "w_q", "w_b", "w_t",
    "capacity_clay", "capacity_gravel", "capacity_organic", "capacity_sand_coarse",
    "capacity_sand_fine", "capacity_sand_medium", "capacity_silt", "capacity_urban", "capacity_stone",
    "field_capacity_clay", "field_capacity_gravel", "field_capacity_organic", "field_capacity_sand_coarse",
    "field_capacity_sand_fine", "field_capacity_sand_medium", "field_capacity_silt", "field_capacity_urban", "field_capacity_stone",
    "w_wetness_percipitation", "w_wetness_soilstore", "gw_init",
    "gw_recharge_factor", "gw_drain_factor", "Gmax", "quickflow_fraction"
]

COMPLEX_MODEL_V2_PARAM_RANGES = {
    "alpha_w": (0.0, 1.0),
    "Idry": (1.0, 500.0),
    "Iwet": (1.0, 100.0),
    "Emax": (1.0, 10.0),
    "perc_rate": (0.001, 0.1),
    "lag_q": (0, 10),
    "lag_b": (10, 30),
    "w_q": (1.0, 10000.0),
    "w_b": (1.0, 10000.0),
    "w_t": (0.0, 1.0),
    # Porosity/saturation values
    "capacity_clay": (0.45, 0.60),
    "capacity_gravel": (0.25, 0.35),
    "capacity_organic": (0.75, 0.90),
    "capacity_sand_coarse": (0.30, 0.39),
    "capacity_sand_fine": (0.33, 0.41),
    "capacity_sand_medium": (0.32, 0.40),
    "capacity_silt": (0.40, 0.50),
    "capacity_urban": (0.35, 0.45),
    "capacity_stone": (0.0, 0.05),
    # Field capacity values
    "field_capacity_clay": (0.32, 0.40),
    "field_capacity_gravel": (0.12, 0.18),
    "field_capacity_organic": (0.40, 0.48),
    "field_capacity_sand_coarse": (0.08, 0.12),
    "field_capacity_sand_fine": (0.12, 0.16),
    "field_capacity_sand_medium": (0.11, 0.15),
    "field_capacity_silt": (0.27, 0.33),
    "field_capacity_urban": (0.13, 0.17),
    "field_capacity_stone": (0.0, 0.01),
    "w_wetness_percipitation": (0.0, 1.0),
    "w_wetness_soilstore": (0.0, 1.0),
    "gw_init": (0.0, 1000.0),
    "gw_recharge_factor": (0.01, 0.5),
    "gw_drain_factor": (0.01, 0.5),
    "Gmax": (100.0, 1000.0),
    "quickflow_fraction": (0.01, 0.5)  # Allow 1% to 50% of precipitation to always go to quick flow
}

COMPLEX_MODEL_V2_INITIAL_PARAMS = {
    "alpha_w": 0.5,
    "Idry": 250.0,
    "Iwet": 50.0,
    "Emax": 5.0,
    "perc_rate": 0.01,
    "lag_q": 5,
    "lag_b": 15,
    "w_q": 1.0,
    "w_b": 1.0,
    "w_t": 0.5,
    "capacity_clay": 0.525,
    "capacity_gravel": 0.30,
    "capacity_organic": 0.825,
    "capacity_sand_coarse": 0.345,
    "capacity_sand_fine": 0.37,
    "capacity_sand_medium": 0.36,
    "capacity_silt": 0.45,
    "capacity_urban": 0.40,
    "capacity_stone": 0.0,
    "field_capacity_clay": 0.36,
    "field_capacity_gravel": 0.15,
    "field_capacity_organic": 0.44,
    "field_capacity_sand_coarse": 0.10,
    "field_capacity_sand_fine": 0.14,
    "field_capacity_sand_medium": 0.13,
    "field_capacity_silt": 0.30,
    "field_capacity_urban": 0.15,
    "field_capacity_stone": 0.0,
    "w_wetness_percipitation": 0.5,
    "w_wetness_soilstore": 0.5,
    "gw_init": 250.0,
    "gw_recharge_factor": 0.1,
    "gw_drain_factor": 0.05,
    "Gmax": 500.0,
    "quickflow_fraction": 0.1  # Default 10% always goes to quick flow
}

COMPLEX_MODEL_V2_PARAM_STEPS = {
    "alpha_w": 0.05,
    "Idry": 10.0,
    "Iwet": 2.0,
    "Emax": 0.5,
    "perc_rate": 0.001,
    "lag_q": 1,
    "lag_b": 1,
    "w_q": 1,
    "w_b": 1,
    "w_t": 0.05,
    "capacity_clay": 0.01,
    "capacity_gravel": 0.01,
    "capacity_organic": 0.01,
    "capacity_sand_coarse": 0.01,
    "capacity_sand_fine": 0.01,
    "capacity_sand_medium": 0.01,
    "capacity_silt": 0.01,
    "capacity_urban": 0.01,
    "capacity_stone": 0.01,
    "field_capacity_clay": 0.01,
    "field_capacity_gravel": 0.01,
    "field_capacity_organic": 0.01,
    "field_capacity_sand_coarse": 0.01,
    "field_capacity_sand_fine": 0.01,
    "field_capacity_sand_medium": 0.01,
    "field_capacity_silt": 0.01,
    "field_capacity_urban": 0.01,
    "field_capacity_stone": 0.01,
    "w_wetness_percipitation": 0.05,
    "w_wetness_soilstore": 0.05,
    "gw_init": 50.0,
    "gw_recharge_factor": 0.01,
    "gw_drain_factor": 0.01,
    "Gmax": 50.0,
    "quickflow_fraction": 0.01
}

SOIL_PERCENTAGES = {
    "Maarssen": {
        "clay": 0.03,
        "gravel": 0,
        "organic": 0.13,
        "sand_coarse": 0.09,
        "sand_fine": 0.22,
        "sand_medium": 0.14,
        "silt": 0.06,
        "urban": 0.50,
        "water": 0.02,
        "stone": 0
    },
    "Millingen": {
        "clay": 0,
        "gravel": 0,
        "organic": 0,
        "sand_coarse": 0.01,
        "sand_fine": 0.01,
        "sand_medium": 0.45,
        "silt": 0.27,
        "urban": 0.01,
        "water": 0.01,
        "stone": 0.0
    },
    "Ommen": {
        "clay": 0,
        "gravel": 0,
        "organic": 0.20,
        "sand_coarse": 0.03,
        "sand_fine": 0.04,
        "sand_medium": 0.65,
        "silt": 0.01,
        "urban": 0.02,
        "water": 0.01,
        "stone": 0
    },
    "Weesp": {
        "clay": 0.31,
        "gravel": 0,
        "organic": 0.46,
        "sand_coarse": 0.01,
        "sand_fine": 0.01,
        "sand_medium": 0.05,
        "silt": 0.04,
        "urban": 0.1,
        "water": 0.03,
        "stone": 0
    }
}

def generate_initial_params(param_ranges, percent):
    params = {}
    for k, v in param_ranges.items():
        if isinstance(v[0], (int, float)) and isinstance(v[1], (int, float)):
            val = v[0] + percent * (v[1] - v[0])
            if isinstance(v[0], int) and isinstance(v[1], int):
                val = int(round(val))
            params[k] = val
    return params

SIMPLE_MODEL_INITIAL_PARAMS_25 = generate_initial_params(SIMPLE_MODEL_PARAM_RANGES, 0.25)
SIMPLE_MODEL_INITIAL_PARAMS_50 = generate_initial_params(SIMPLE_MODEL_PARAM_RANGES, 0.5)
SIMPLE_MODEL_INITIAL_PARAMS_75 = generate_initial_params(SIMPLE_MODEL_PARAM_RANGES, 0.75)

COMPLEX_MODEL_INITIAL_PARAMS_25 = generate_initial_params(COMPLEX_MODEL_PARAM_RANGES, 0.25)
COMPLEX_MODEL_INITIAL_PARAMS_50 = generate_initial_params(COMPLEX_MODEL_PARAM_RANGES, 0.5)
COMPLEX_MODEL_INITIAL_PARAMS_75 = generate_initial_params(COMPLEX_MODEL_PARAM_RANGES, 0.75)

COMPLEX_MODEL_INITIAL_PARAMS_V2_25 = generate_initial_params(COMPLEX_MODEL_V2_PARAM_RANGES, 0.25)
COMPLEX_MODEL_INITIAL_PARAMS_V2_50 = generate_initial_params(COMPLEX_MODEL_V2_PARAM_RANGES, 0.5)
COMPLEX_MODEL_INITIAL_PARAMS_V2_75 = generate_initial_params(COMPLEX_MODEL_V2_PARAM_RANGES, 0.75)
