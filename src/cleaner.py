import numpy as np
import pandas as pd
from fontTools.feaLib import location


class DataCleaner():
    def __init__(self):
        pass

    @staticmethod
    def rws_discharge_cleaner(path: str) -> pd.DataFrame:

        df = pd.read_csv(path, sep = None, engine = "python")

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

        # Rename the column such we can easily combine them later on.
        result = result.rename(columns={'WAARNEMINGDATUM': 'YYYYMMDD'})
        result['YYYYMMDD'] = pd.to_datetime(result['YYYYMMDD'], format='%d-%m-%Y')

        return result

    @staticmethod
    def knmi_cleaner(path: str, skip_to_line: int) -> pd.DataFrame:
        # Setup the start and enddate
        startdate = pd.to_datetime("2020-09-21")
        enddate = pd.to_datetime("2023-09-20")

        # Read txt to dataframe in pandas
        df = pd.read_csv(path, skiprows=skip_to_line)

        # Remove redundant spaces in column names
        df.columns = df.columns.str.strip()

        # Set the date column to a date field
        df['YYYYMMDD'] = pd.to_datetime(df['YYYYMMDD'], format='%Y%m%d')

        # Drop columns that only contain NaN values and the station numbers as we don't need them
        df = df.dropna(axis=1, how='all')

        # Only keep data for the dates we are interested in
        mask = (df['YYYYMMDD'] >= startdate) & (df['YYYYMMDD'] < enddate)
        df = df.loc[mask]

        return df

    def soil_data_cleaner(self, path: str, location: str) -> pd.DataFrame:
        df = pd.read_csv(path)
        filtered_df = df[df["MEETPUNT_IDENTIFICATIE"] == location]
        pivoted_df = filtered_df.pivot(
            index='MEETPUNT_IDENTIFICATIE',
            columns='soil_category',
            values='area'
        ).reset_index()

        return pivoted_df