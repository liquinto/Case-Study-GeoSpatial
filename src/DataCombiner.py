import pandas as pd

class DataCombiner(object):
    def __init__(self):
        pass

    def combine(self, data_frames: list[pd.DataFrame]) -> pd.DataFrame:
        sorted_data_frames = sorted(data_frames, key=len, reverse=True)

        # Start with the first (largest) dataframe
        final_data_frame = sorted_data_frames[0].copy()

        # Merge the remaining dataframes one by one
        for df in sorted_data_frames[1:]:
            final_data_frame = final_data_frame.merge(df, on="YYYYMMDD", how='inner')

        return final_data_frame