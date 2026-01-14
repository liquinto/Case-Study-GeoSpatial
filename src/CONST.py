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