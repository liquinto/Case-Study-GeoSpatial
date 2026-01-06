from SimpleModel import SimpleModel
import pandas as pd

def main():
    model = SimpleModel(
        alpha_w=0.9,
        Idry=25.0,
        Iwet=3.0,
        Smax=200.0,
        Emax=5.0,
        perc_rate=0.03,
        lag_q=2,
        lag_b=10,
        w_q=0.6,
        w_b=0.4,
    )
    df = pd.read_csv("../data/cleaned/Maarssen.csv")
    results = model.run_dataframe(
        df=df,
        pt_col="RD",
        pet_col="EV24",
        q0=0.0
    )
    results_df = pd.DataFrame(results)
    results_df["date"] = df["YYYYMMDD"].values
    results_df.to_csv(path_or_buf="../data/results/Maarssen.csv", index=False)

if __name__ == "__main__":
    main()


