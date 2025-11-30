import pandas as pd

from cleaner import DataCleaner
from typing import Optional

from src.DataCombiner import DataCombiner


def main():
    '''
    This function will perform the following steps:
    1. Load in all the data.
    2. Clean all the data.
    3. Combine all the data into a single dataframe.
    4. Write the data to a csv file.
    '''
    airtemp_dir = "../data/airtemp/"
    discharge_dir = "../data/discharge/"
    rain_dir = "../data/rainfall/"
    soil_dir = "../data/soil_type/"
    cleaned_dir = "../data/cleaned/"

    cleaner = DataCleaner()

    maarssen: dict[str, pd.DataFrame] = {
        "soil_type": cleaner.soil_data_cleaner(f"{soil_dir}soil_type.csv", "Maarssen"),
        "rainfall": cleaner.knmi_cleaner(f"{rain_dir}De Bilt.txt", 22),
        "airtemp": cleaner.knmi_cleaner(f"{airtemp_dir}De Bilt.txt", 50),
        "discharge": cleaner.rws_discharge_cleaner(f"{discharge_dir}Maarsen.csv"),
    }

    millingen: dict[str, Optional[pd.DataFrame]] = {
        "soil_type": cleaner.soil_data_cleaner(f"{soil_dir}soil_type.csv", "Lobith"),
        "rainfall": cleaner.knmi_cleaner(f"{rain_dir}Volkel.txt", 22),
        "airtemp": cleaner.knmi_cleaner(f"{airtemp_dir}Volkel.txt", 50),
        "discharge": cleaner.rws_discharge_cleaner(f"{discharge_dir}Millingen.csv"),
    }

    ommen: dict[str, Optional[pd.DataFrame]] = {
        "soil_type": cleaner.soil_data_cleaner(f"{soil_dir}soil_type.csv", "Ommen Hesselmulertbrug"),
        "rainfall": cleaner.knmi_cleaner(f"{rain_dir}Hoogeveen.txt", 22),
        "airtemp": cleaner.knmi_cleaner(f"{airtemp_dir}Hoogeveen.txt", 50),
        "discharge": cleaner.rws_discharge_cleaner(f"{discharge_dir}Ommen.csv"),
    }

    weesp: dict[str, Optional[pd.DataFrame]] = {
        "soil_type": cleaner.soil_data_cleaner(f"{soil_dir}soil_type.csv", "Weesp West"),
        "rainfall": cleaner.knmi_cleaner(f"{rain_dir}Weesp.txt", 22),
        "airtemp": cleaner.knmi_cleaner(f"{airtemp_dir}Schiphol.txt", 50),
        "discharge": cleaner.rws_discharge_cleaner(f"{discharge_dir}Weesp.csv"),
    }

    data_combiner = DataCombiner()

    maarssen_df = data_combiner.combine([maarssen["rainfall"], maarssen["airtemp"], maarssen["discharge"]])
    millingen_df = data_combiner.combine([millingen["rainfall"], millingen["airtemp"], millingen["discharge"]])
    ommen_df = data_combiner.combine([ommen["rainfall"], ommen["airtemp"], ommen["discharge"]])
    weesp_df = data_combiner.combine([weesp["rainfall"], weesp["airtemp"], weesp["discharge"]])

    for col in maarssen["soil_type"].columns:
        if col != 'MEETPUNT_IDENTIFICATIE':
            maarssen_df[col] = maarssen["soil_type"][col].values[0]

    for col in millingen["soil_type"].columns:
        if col != 'MEETPUNT_IDENTIFICATIE':
            millingen_df[col] = millingen["soil_type"][col].values[0]

    for col in ommen["soil_type"].columns:
        if col != 'MEETPUNT_IDENTIFICATIE':
            ommen_df[col] = ommen["soil_type"][col].values[0]

    for col in weesp["soil_type"].columns:
        if col != 'MEETPUNT_IDENTIFICATIE':
            weesp_df[col] = weesp["soil_type"][col].values[0]

    maarssen_df.to_csv(f'{cleaned_dir}Maarssen', index=False)
    millingen_df.to_csv(f'{cleaned_dir}Millingen', index=False)
    ommen_df.to_csv(f'{cleaned_dir}Ommen', index=False)
    weesp_df.to_csv(f'{cleaned_dir}Weesp', index=False)


if __name__ == "__main__":
    main()