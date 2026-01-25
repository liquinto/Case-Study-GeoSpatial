import pandas as pd

from BaseModel import BaseModel
from ComplexModel_V2 import ComplexModel_V2
from sklearn.metrics import mean_squared_error
from model_calibrator import ModelCalibrator
from CONST import *

def main():
    df = pd.read_csv("../data/cleaned/Weesp.csv")

    calibrator = ModelCalibrator(
        model_class=ComplexModel_V2,
        param_names=COMPLEX_MODEL_V2_PARAM_NAMES,
        param_ranges=COMPLEX_MODEL_V2_PARAM_RANGES,
        param_steps=COMPLEX_MODEL_V2_PARAM_STEPS,
        score_func=ComplexModel_V2.score,
        max_iter=10000
    )
    best_params, best_score = calibrator.calibrate(
        fixed_params={"location": "Weesp"},
        tune_params_init=COMPLEX_MODEL_INITIAL_PARAMS_V2_50,
        df=df,
        target=df["ALFANUMERIEKEWAARDE"],
        q_col="Q",
        n=31,
        pt_col="RD",
        pet_col="EV24",
        q0=0.0
    )
    print("Best parameters for ComplexModel:", {k: round(v, 2) for k, v in best_params.items()})
    print("Best MSE after calibration:", best_score)

    basemodel = BaseModel()
    basemodel.fit(X = df, y = df["ALFANUMERIEKEWAARDE"])
    result_df_basemodel = basemodel.predict(X = df)
    print(f'MSE Base Model: {mean_squared_error(df["ALFANUMERIEKEWAARDE"], result_df_basemodel)}')

    print("Running on new data with calibrated SimpleModel...")
    df_new = pd.read_csv("../data/test_data/Weesp.csv")
    complex_model_v2 = ComplexModel_V2(**best_params)
    score = complex_model_v2.score(
        df=df_new,
        target=df_new["ALFANUMERIEKEWAARDE"],
        q_col="Q",
        n=1,
        pt_col="RD",
        pet_col="EV24",
        q0=0.0
    )
    print("MSE on new data with calibrated SimpleModel:", score)
    result_df_basemodel = basemodel.predict(X=df_new)
    print(f'MSE Base Model on Test Data: {mean_squared_error(df_new["ALFANUMERIEKEWAARDE"], result_df_basemodel)}')


if __name__ == "__main__":
    main()
