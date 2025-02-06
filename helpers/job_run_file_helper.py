"""Job run file helper"""
import os
import pandas as pd
from helpers.enums import DataModule
from helpers.pandas_helper import PandasHelper
from settings.file_settings import FileSettings


class JobRunFileHelper():
    """Job run file helper"""

    def __init__(self) -> None:
        self.pandas_helper = PandasHelper()

    def get_run_file_path(self, run_id: str, module: DataModule):
        """get run file path"""
        file_name = f"{module.name.lower()}.csv"
        return os.path.join(FileSettings.DATA_ROOT_PATH, run_id, file_name)

    def save_run_file_to_csv(
        self, dataframe: pd.DataFrame, run_id: str, module: DataModule
    ):
        """save run file dataframe to csv"""
        file_path = self.get_run_file_path(run_id, module)
        self.pandas_helper.save_df_to_csv(dataframe, file_path)

    def read_run_file(self, run_id: str, module: DataModule):
        """read run file"""
        file_path = self.get_run_file_path(run_id, module)
        return pd.read_csv(file_path)
