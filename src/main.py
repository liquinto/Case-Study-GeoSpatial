from SimpleModel import SimpleModel
from BaseModel import BaseModel
import pandas as pd
from sklearn.metrics import mean_squared_error

def main():
    model = SimpleModel(
        alpha_w=0.6,
        Idry=250.0,
        Iwet=30.0,
        Smax=800.0,
        Emax=5.0,
        perc_rate=0.01,
        lag_q=0,
        lag_b=5,
        w_q=0.1,
        w_b=0.85,
        w_t=0.9
    )
    df = pd.read_csv("../data/cleaned/Millingen.csv")
    results = model.run_dataframe(
        df=df,
        pt_col="RD",
        pet_col="EV24",
        q0=0.0
    )
    results_df = pd.DataFrame(results)
    results_df["date"] = df["YYYYMMDD"].values
    results_df.to_csv(path_or_buf="../data/results/Millingen.csv", index=False)

    print(f'MSE Simple Model: {mean_squared_error(df["ALFANUMERIEKEWAARDE"][:31], results_df["Q"][:31])}')

    basemodel = BaseModel()
    basemodel.fit(X = df, y = df["ALFANUMERIEKEWAARDE"])
    result_df_basemodel = basemodel.predict(X = df)
    print(f'MSE Base Model: {mean_squared_error(df["ALFANUMERIEKEWAARDE"], result_df_basemodel)}')


if __name__ == "__main__":
    main()


