import pandas as pd
import numpy as np
from SimpleModel import SimpleModel
from ComplexModel import ComplexModel
from CONST import (
    SIMPLE_MODEL_PARAM_NAMES, SIMPLE_MODEL_INITIAL_PARAMS, SIMPLE_MODEL_PARAM_RANGES,
    COMPLEX_MODEL_PARAM_NAMES, COMPLEX_MODEL_INITIAL_PARAMS, COMPLEX_MODEL_PARAM_RANGES,
    COMPLEX_MODEL_V2_INITIAL_PARAMS, COMPLEX_MODEL_V2_PARAM_RANGES, COMPLEX_MODEL_V2_PARAM_NAMES
)
import os

from src.ComplexModel_V2 import ComplexModel_V2

# Settings
data_path = '../data/cleaned/Maarssen.csv'
target_col = 'ALFANUMERIEKEWAARDE'
pt_col = 'RD'
pet_col = 'EV24'
n = 31
q0 = 0.0
location = 'Maarssen'

# Load data
df = pd.read_csv(data_path)
target = df[target_col]

def compute_mse_simple(params):
    model = SimpleModel(**params)
    results = model.run_dataframe(df, pt_col=pt_col, pet_col=pet_col, q0=q0)
    results_df = pd.DataFrame(results)
    return np.mean((target[:n] - results_df['Q'][:n]) ** 2)

def compute_mse_complex(params):
    model = ComplexModel_V2(**params)
    results = model.run_dataframe(df, pt_col=pt_col, pet_col=pet_col, q0=q0)
    results_df = pd.DataFrame(results)
    return np.mean((target[:n] - results_df['Q'][:n]) ** 2)

def sensitivity_analysis(param_names, initial_params, param_ranges, compute_mse_func):
    base_params = initial_params.copy()
    base_mse = compute_mse_func(base_params)
    results = []
    for param in param_names:
        if param not in param_ranges:
            continue
        pmin, pmax = param_ranges[param]
        pval = base_params[param]
        is_int = isinstance(pmin, int) and isinstance(pmax, int)
        # +10% shift
        pval_up = pval * 1.1
        pval_up = min(pval_up, pmax)
        if is_int:
            pval_up = int(round(pval_up))
        params_up = base_params.copy()
        params_up[param] = pval_up
        mse_up = compute_mse_func(params_up)
        # -10% shift
        pval_down = pval * 0.9
        pval_down = max(pval_down, pmin)
        if is_int:
            pval_down = int(round(pval_down))
        params_down = base_params.copy()
        params_down[param] = pval_down
        mse_down = compute_mse_func(params_down)
        # Importance: max absolute change
        importance = max(abs(mse_up - base_mse), abs(mse_down - base_mse))
        results.append({'parameter': param, 'base_value': pval, 'mse': base_mse,
                        'mse_up': mse_up, 'mse_down': mse_down, 'importance': importance})
    df_result = pd.DataFrame(results)
    df_result = df_result.sort_values('importance', ascending=False).reset_index(drop=True)
    return df_result

def cast_int_params(params, param_ranges):
    for k, v in params.items():
        if k in param_ranges:
            pmin, pmax = param_ranges[k]
            if isinstance(pmin, int) and isinstance(pmax, int):
                params[k] = int(round(v))
    return params

if __name__ == '__main__':
    print('Running sensitivity analysis for SimpleModel...')
    simple_params = cast_int_params(SIMPLE_MODEL_INITIAL_PARAMS.copy(), SIMPLE_MODEL_PARAM_RANGES)
    df_simple = sensitivity_analysis(
        SIMPLE_MODEL_PARAM_NAMES,
        simple_params,
        SIMPLE_MODEL_PARAM_RANGES,
        compute_mse_simple
    )
    df_simple['model'] = 'SimpleModel'
    print(df_simple)
    print('\nRunning sensitivity analysis for ComplexModel...')
    complex_params = cast_int_params(COMPLEX_MODEL_V2_INITIAL_PARAMS.copy(), COMPLEX_MODEL_V2_PARAM_RANGES)
    complex_params['location'] = location  # Ensure location is set
    df_complex = sensitivity_analysis(
        COMPLEX_MODEL_V2_PARAM_NAMES,
        complex_params,
        COMPLEX_MODEL_V2_PARAM_RANGES,
        compute_mse_complex
    )
    df_complex['model'] = 'ComplexModel'
    print(df_complex)

    # Save to CSV
    out_path = '../data/sensitivity/sensitivity_Maarssen.csv'
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df_out = pd.concat([df_simple, df_complex], ignore_index=True)
    df_out.to_csv(out_path, index=False)
    print(f'Written combined sensitivity results to {out_path}')
