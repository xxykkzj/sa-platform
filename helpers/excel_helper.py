"""Excel helper module"""
import logging
import pandas as pd

from helpers.file_helper import FileHelper


class ExcelHelper():
    """Excel Helper class"""

    def __init__(self) -> None:
        self.file_helper = FileHelper()
        self.logger = logging.getLogger(__name__)

    def get_writer(self, file_path: str):
        """Get instance of excel writer"""
        excel_engine = "openpyxl"
        if self.file_helper.does_file_exist(file_path):
            return pd.ExcelWriter(file_path,
                                  engine=excel_engine,
                                  mode="a",
                                  if_sheet_exists="overlay")

        return pd.ExcelWriter(file_path, engine=excel_engine)

    def write_to_excel(self, file_path: str, data: list, sheet_name: str):
        """Write list data to excel"""
        log_msg = f"file_path: {file_path}. sheet_name: {sheet_name}"
        self.logger.info("Writing to excel. %s", log_msg)

        self.file_helper.make_directories_from_file_path(file_path)

        with self.get_writer(file_path) as writer:
            current_sheet = writer.sheets.get(sheet_name)
            max_row = 0
            header = True
            if current_sheet:
                max_row = current_sheet.max_row
                header = None
            pd.DataFrame(data).to_excel(
                writer,
                sheet_name=sheet_name,
                index=False,
                startrow=max_row,
                header=header)
