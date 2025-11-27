import numpy as np
import pandas as pd

class DataCleaner():
    def __init__(self):
        pass

    @staticmethod
    def rws_clean_df(df: pd.DataFrame) -> pd.DataFrame:
        # Only include data that is annotated to be a normal value
        df = df[df["KWALITEITSOORDEEL_CODE"] == "Normale waarde"]

        # Keep only the columns that we are interested in
        data = df[["MEETPUNT_IDENTIFICATIE", "WAARNEMINGDATUM", "WAARNEMINGTIJD (MET/CET)", "ALFANUMERIEKEWAARDE"]].copy()

        # Change the column: 'ALFANUMERIEKEWAARDE' to be a float value
        data["ALFANUMERIEKEWAARDE"] = data["ALFANUMERIEKEWAARDE"].astype(float)

        # Find the mean value of the discharge in a day and only keep 1 entry for a day
        result = data.groupby(["WAARNEMINGDATUM"], as_index=False)["ALFANUMERIEKEWAARDE"].mean()
        
        # Round of the value of discharge to have 2
        result["ALFANUMERIEKEWAARDE"]= result["ALFANUMERIEKEWAARDE"].round(2)

        return result


