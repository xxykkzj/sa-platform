"""
Helper methods for pandas library
"""

import os
import pandas as pd
from helpers.file_helper import FileHelper


class PandasHelper:
    """
    Pandas helper
    """

    def __init__(self) -> None:
        self.numeric_columns = ["sessions"]
        self.date_time_columns = ["start_date", "end_date"]
        self.file_helper = FileHelper()

    def convert_data_types(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """convert data types"""
        for num_col in self.numeric_columns:
            if num_col in dataframe.columns:
                dataframe[num_col] = pd.to_numeric(dataframe[num_col])

        for date_col in self.date_time_columns:
            if date_col in dataframe.columns:
                dataframe[date_col] = pd.to_datetime(dataframe[date_col])

        return dataframe

    def save_list_to_csv(self, data: list, file_path):
        """save list of data as csv"""
        self.file_helper.create_directory(os.path.dirname(file_path))
        dataframe = pd.DataFrame(data)
        dataframe.to_csv(file_path, index=False)

    def save_df_to_csv(self, dataframe: pd.DataFrame, file_path: str):
        """save dataframe to csv"""
        self.file_helper.create_directory_excluding_filename(file_path)
        dataframe.to_csv(file_path, index=False)
