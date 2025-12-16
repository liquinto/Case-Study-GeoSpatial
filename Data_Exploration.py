from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

SINGLE_FILE_PATH = "Maarssen" 
def _read_any(path):
    try:
        return pd.read_csv(path, sep=None, engine="python")
    except Exception:
        return pd.read_csv(path)

def _parse_date(df):
    candidates = [c for c in ["YYYYMMDD","Date","DATE","date","DATUM"] if c in df.columns]
    if not candidates:
        raise ValueError("No date column found (expected YYYYMMDD/Date/date/DATUM).")
    col = candidates[0]
    if str(df[col].dtype).startswith(("int","float")):
        df["date"] = pd.to_datetime(df[col].astype(str), format="%Y%m%d", errors="coerce")
    else:
        df["date"] = pd.to_datetime(df[col], errors="coerce", dayfirst=False)
    df.drop(columns=[col], inplace=True)
    return df

def rename_to_descriptions(df):
    """Rename KNMI + appended columns to human-readable descriptions (with units/EN translations)."""
    desc_map = {
        # Core time/id
        "YYYYMMDD": "Date (Year-Month-Day)",
        "STN": "Station number",
        "# STN": "Station number (2)",

        # Wind / temp / radiation / precip / pressure / humidity / visibility
        "DDVEC": "Vector mean wind direction (degrees; 360=N, 90=E, 180=S, 270=W, 0=calm/variable)",
        "FHVEC": "Vector mean windspeed (0.1 m/s)",
        "FG":    "Daily mean windspeed (0.1 m/s)",
        "FHX":   "Maximum hourly mean windspeed (0.1 m/s)",
        "FHXH":  "Hour of FHX (hour)",
        "FHN":   "Minimum hourly mean windspeed (0.1 m/s)",
        "FHNH":  "Hour of FHN (hour)",
        "FXX":   "Maximum wind gust (0.1 m/s)",
        "FXXH":  "Hour of FXX (hour)",
        "TG":    "Daily mean temperature (0.1 °C)",
        "TN":    "Minimum temperature (0.1 °C)",
        "TNH":   "Hour of TN (hour)",
        "TX":    "Maximum temperature (0.1 °C)",
        "TXH":   "Hour of TX (hour)",
        "T10N":  "Min temperature at 10 cm (0.1 °C)",
        "T10NH": "6-hour division of T10N (6=0–6,12=6–12,18=12–18,24=18–24 UT)",
        "SQ":    "Sunshine duration from radiation (0.1 h; -1 for <0.05 h)",
        "SP":    "Percent of potential sunshine duration (%)",
        "Q":     "Global radiation (J/cm²)",
        "DR":    "Precipitation duration (0.1 h)",
        "RH":    "Daily precipitation amount (0.1 mm; -1 for <0.05 mm)",
        "RHX":   "Max hourly precipitation (0.1 mm; -1 for <0.05 mm)",
        "RHXH":  "Hour of RHX (hour)",
        "PG":    "Daily mean sea level pressure (0.1 hPa)",
        "PX":    "Max hourly sea level pressure (0.1 hPa)",
        "PXH":   "Hour of PX (hour)",
        "PN":    "Min hourly sea level pressure (0.1 hPa)",
        "PNH":   "Hour of PN (hour)",
        "VVN":   "Minimum visibility (coded scale)",
        "VVNH":  "Hour of VVN (hour)",
        "VVX":   "Maximum visibility (coded scale)",
        "VVXH":  "Hour of VVX (hour)",
        "NG":    "Mean daily cloud cover (octants; 0–8, 9=sky invisible)",
        "UG":    "Daily mean relative humidity (%)",
        "UX":    "Maximum relative humidity (%)",
        "UXH":   "Hour of UX (hour)",
        "UN":    "Minimum relative humidity (%)",
        "UNH":   "Hour of UN (hour)",
        "EV24":  "Potential evapotranspiration (Makkink) (0.1 mm)",

        # Precip & snow table headers
        "RD":    "24-h precipitation 08–08 UTC (0.1 mm)",
        "SX":    "Snow cover code at 08:00 UTC (coded)",

        # Discharge 
        "ALFANUMERIEKEWAARDE": "Discharge (m³/s)",

        # Dutch soil / land-cover columns → English
        "Bebouwd gebied":          "Built-up area",
        "Dikke eerdgronden":       "Thick eerd soils (plaggen)",
        "Ingewikkelde samenstelling": "Complex composition (mixed soils)",
        "Kalkloze zandgronden":    "Non-calcareous sandy soils",
        "Moerige gronden":         "Humic/peaty soils",
        "Podzolgronden":           "Podzol soils",
        "Rivierkleigronden":       "River clay soils",
        "Veengronden":             "Peat soils",
        "Water":                   "Water",
    }

    new_cols, seen = [], {}
    for c in df.columns:
        new_name = desc_map.get(c, c)
        if new_name in seen:
            seen[new_name] += 1
            new_name = f"{new_name} ({seen[new_name]})"
        else:
            seen[new_name] = 1
        new_cols.append(new_name)

    out = df.copy()
    out.columns = new_cols
    return out

def load_table(path):
    df = _read_any(path)
    df = _parse_date(df)
    df = rename_to_descriptions(df)

    rd = "24-h precipitation 08–08 UTC (0.1 mm)"
    rh = "Daily precipitation amount (0.1 mm; -1 for <0.05 mm)"
    if "p_mm" not in df.columns:
        if rd in df.columns:
            df["p_mm"] = df[rd]
        elif rh in df.columns:
            df["p_mm"] = df[rh]

    if "q_m3s" not in df.columns and "Discharge (m³/s)" in df.columns:
        df["q_m3s"] = df["Discharge (m³/s)"]

    if "tmean_c" not in df.columns and "Daily mean temperature (0.1 °C)" in df.columns:
        df["tmean_c"] = df["Daily mean temperature (0.1 °C)"]

    if "pet_mm" not in df.columns and "Potential evapotranspiration (Makkink) (0.1 mm)" in df.columns:
        df["pet_mm"] = df["Potential evapotranspiration (Makkink) (0.1 mm)"]

    df = (df.dropna(subset=["date"])
            .drop_duplicates(subset=["date"])
            .sort_values("date")
            .reset_index(drop=True))
    return df

def print_basic_info(df):
    print("\n=== BASIC INFO ===")
    print(f"Rows: {len(df)}, Columns: {len(df.columns)}")
    print("Columns:", list(df.columns))
    print("Date range:", df["date"].min().date(), "→", df["date"].max().date())
    print("\nHead:\n", df.head(10).to_string(index=False))
    print("\nTail:\n", df.tail(10).to_string(index=False))

def print_describe(df):
    num = df.select_dtypes("number")
    if num.empty:
        print("\n(No numeric columns to describe.)")
        return
    print("\n=== SUMMARY STATS (numeric) ===")
    print(num.describe().T.to_string())

def print_monthly_stats(df):
    dfm = df.copy()
    dfm["month"] = dfm["date"].dt.to_period("M").astype(str)
    outs = []
    if "p_mm" in dfm:
        outs.append(dfm.groupby("month")["p_mm"].sum().rename("P_monthly_sum_mm"))
    if "q_m3s" in dfm:
        outs.append(dfm.groupby("month")["q_m3s"].mean().rename("Q_monthly_mean_m3s"))
    if "tmean_c" in dfm:
        outs.append(dfm.groupby("month")["tmean_c"].mean().rename("T_monthly_mean_C"))
    if outs:
        res = pd.concat(outs, axis=1)
        print("\n=== MONTHLY STATS ===")
        print(res.round(2).to_string())
    else:
        print("\n(No P/Q/T columns for monthly stats.)")

def show_timeseries(df):
    dfi = df.set_index("date")
    plots_shown = False
    if "q_m3s" in dfi:
        dfi["q_m3s"].plot(title="Discharge (Q) — daily")
        plt.tight_layout(); plt.show(); plots_shown=True
        dfi["q_m3s"].resample("M").mean().plot(title="Discharge (Q) — monthly mean")
        plt.tight_layout(); plt.show()
    if "p_mm" in dfi:
        dfi["p_mm"].plot(title="Precipitation (P) — daily")
        plt.tight_layout(); plt.show(); plots_shown=True
        dfi["p_mm"].resample("M").sum().plot(title="Precipitation (P) — monthly sum")
        plt.tight_layout(); plt.show()
    if "pet_mm" in dfi:
        dfi["pet_mm"].plot(title="Potential ET (PET) — daily")
        plt.tight_layout(); plt.show(); plots_shown=True
    if "tmean_c" in dfi:
        dfi["tmean_c"].plot(title="Temperature (Tmean) — daily")
        plt.tight_layout(); plt.show(); plots_shown=True
    if not plots_shown:
        print("\n(No standard meteo/Q columns to plot as time series.)")

def show_histograms(df):
    for col in ["q_m3s","p_mm","pet_mm","tmean_c"]:
        if col in df.columns:
            df[col].dropna().hist(bins=40)
            plt.title(f"Histogram — {col}")
            plt.tight_layout(); plt.show()

def show_monthly_boxplots(df):
    dfm = df.copy()
    dfm["month"] = dfm["date"].dt.month
    if "q_m3s" in dfm:
        dfm.boxplot(column="q_m3s", by="month")
        plt.title("Q by month"); plt.suptitle(""); plt.tight_layout(); plt.show()
    if "p_mm" in dfm:
        dfm.boxplot(column="p_mm", by="month")
        plt.title("P by month"); plt.suptitle(""); plt.tight_layout(); plt.show()

def show_correlation_heatmap(df):
    num = df.select_dtypes("number")
    if num.shape[1] == 0:
        print("\n(No numeric columns for correlations.)")
        return
    corr = num.corr()
    print("\n=== CORRELATION MATRIX (numeric) ===")
    print(corr.round(3).to_string())
    plt.figure(figsize=(8,6))
    plt.imshow(corr, aspect="auto")
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
    plt.yticks(range(len(corr.index)), corr.index)
    plt.title("Correlation matrix")
    plt.colorbar()
    plt.tight_layout(); plt.show()


def print_top_correlations(df, top_n=10, method="pearson"):
    """Print top absolute correlations between numeric columns, excluding 1.0 and duplicates."""
    num = df.select_dtypes(include=[np.number])
    if num.shape[1] < 2:
        print("Not enough numeric columns for pairwise correlations.")
        return
    corr = num.corr(method=method)

    # keep only upper triangle (no dupes), drop diagonal, drop perfect |r|=1
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    pairs = corr.where(mask).stack().reset_index()
    pairs.columns = ["var1", "var2", "corr"]
    pairs["abs_corr"] = pairs["corr"].abs()
    pairs = pairs[pairs["abs_corr"] < 0.9999]  # exclude perfect 1.0

    if pairs.empty:
        print("No non-trivial correlations found.")
        return

    pairs = pairs.sort_values("abs_corr", ascending=False).head(top_n)
    print(f"\nTop {len(pairs)} absolute correlations (excluding 1.0):")
    print(pairs.to_string(index=False, formatters={"corr": "{:.3f}".format,
                                                   "abs_corr": "{:.3f}".format}))

def print_outliers(df, q=0.99):
    if "q_m3s" in df.columns:
        thr_q = df["q_m3s"].quantile(q)
        top_q = df.loc[df["q_m3s"] >= thr_q, ["date","q_m3s"]].sort_values("q_m3s", ascending=False)
        print(f"\n=== Top {int((1-q)*100)}% Q days (threshold {thr_q:.2f} m3/s) ===")
        print(top_q.head(15).to_string(index=False))
    if "p_mm" in df.columns:
        thr_p = df["p_mm"].quantile(q)
        top_p = df.loc[df["p_mm"] >= thr_p, ["date","p_mm"]].sort_values("p_mm", ascending=False)
        print(f"\n=== Top {int((1-q)*100)}% P days (threshold {thr_p:.2f} mm) ===")
        print(top_p.head(15).to_string(index=False))

def print_corr_with_discharge(df, method="pearson", lags=(0,), top_n=20):
    if "q_m3s" not in df.columns:
        print("Column 'q_m3s' not found.")
        return

    num = df.select_dtypes(include=[np.number]).copy()
    if "q_m3s" in num.columns:
        num = num.drop(columns=["q_m3s"])

    q = df["q_m3s"]

    for lag in lags:
        rows = []
        for col in num.columns:
            x = num[col]
            # skip constants (std==0) which would give NaN correlations
            if float(x.std(ddof=0)) == 0.0:
                continue
            x_shift = x.shift(lag)  # X leads Q by 'lag' days
            mask = q.notna() & x_shift.notna()
            if mask.sum() < 3:
                continue
            r = q[mask].corr(x_shift[mask], method=method)
            if pd.isna(r):
                continue
            rows.append((col, r, abs(r)))

        if not rows:
            print(f"\nNo valid correlations for lag={lag} days.")
            continue

        out = (pd.DataFrame(rows, columns=["variable", "corr", "abs_corr"])
                 .sort_values("abs_corr", ascending=False)
                 .head(top_n))

        tag = "same day" if lag == 0 else f"{lag}-day lead (X → Q)"
        print(f"\nTop {len(out)} correlations with Q — {tag}, method={method}")
        print(out[["variable", "corr", "abs_corr"]]
              .to_string(index=False, formatters={"corr":"{:.3f}".format,
                                                 "abs_corr":"{:.3f}".format}))


df = load_table(SINGLE_FILE_PATH)
print(df.columns.tolist())  # check the new human-readable headers

assert df["date"].is_monotonic_increasing, "Dates not sorted."
if "p_mm" in df: 
    assert (df["p_mm"] >= 0).all(), "Negative precipitation found."
if "q_m3s" in df:
    assert df["q_m3s"].notna().mean() > 0.5, "Too many missing Q for EDA."

print_basic_info(df)
print_describe(df)
print_monthly_stats(df)
show_timeseries(df)
show_histograms(df)
show_monthly_boxplots(df)
show_correlation_heatmap(df)
print_top_correlations(df, top_n=15)
print_outliers(df)
print_corr_with_discharge(df, lags=(0,1,2,3,7), top_n=20)

