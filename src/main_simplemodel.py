import pandas as pd

from SimpleModel import SimpleModel
from BaseModel import BaseModel
from sklearn.metrics import mean_squared_error
from model_calibrator import ModelCalibrator
from CONST import *

def main():
    df = pd.read_csv("../data/cleaned/Ommen.csv")

    calibrator = ModelCalibrator(
        model_class=SimpleModel,
        param_names=SIMPLE_MODEL_PARAM_NAMES,
        param_ranges=SIMPLE_MODEL_PARAM_RANGES,
        param_steps=SIMPLE_MODEL_PARAM_STEPS,
        score_func=SimpleModel.score,
        max_iter=100000
    )
    best_params, best_score = calibrator.calibrate(
        fixed_params={},
        tune_params_init=SIMPLE_MODEL_INITIAL_PARAMS_50,
        df=df,
        target=df["ALFANUMERIEKEWAARDE"],
        q_col="Q",
        n=31,
        pt_col="RD",
        pet_col="EV24",
        q0=0.0
    )
    print("Best parameters for SimpleModel:", best_params)
    print("Best MSE after calibration:", best_score)

    basemodel = BaseModel()
    basemodel.fit(X = df, y = df["ALFANUMERIEKEWAARDE"])
    result_df_basemodel = basemodel.predict(X = df)
    print(f'MSE Base Model: {mean_squared_error(df["ALFANUMERIEKEWAARDE"], result_df_basemodel)}')


if __name__ == "__main__":
    main()
