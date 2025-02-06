"""File helpers"""

import os
import shutil
import logging
from datetime import date
from helpers.date_helper import DateHelper
from helpers.string_helper import StringHelper


class FileHelper:
    """helper methods for file handling"""

    def __init__(self) -> None:
        self.string_helper = StringHelper()
        self.date_helper = DateHelper()
        self.logger = logging.getLogger(__name__)

    def create_directory(self, dir_path: str):
        """create directory"""
        os.makedirs(dir_path, exist_ok=True)

    def create_directory_excluding_filename(self, file_path):
        """create directory excluding filename"""
        self.create_directory(os.path.dirname(file_path))

    def get_data_path_in_current_directory(
        self, data_frequency_name, module_name, date_obj: date
    ):
        """get data path in current directory"""
        return self.get_data_path(".", data_frequency_name, module_name, date_obj)

    def get_file_name_based_on_date(self, date_obj: date):
        """get file name based on date"""
        month_str = str(date_obj.month).zfill(2)
        day_str = str(date_obj.day).zfill(2)
        return f"{date_obj.year}_{month_str}_{day_str}"

    def get_data_path(
        self, root_dir, data_frequency_name: str, module_name: str, date_obj: date
    ):
        """get data path
        Note: cannot have DataFrequency object because of circular dependency
        """
        month_str = str(date_obj.month).zfill(2)
        day_str = str(date_obj.day).zfill(2)
        data_dir_path = os.path.join(
            root_dir,
            "data",
            data_frequency_name,
            module_name,
            str(date_obj.year),
            month_str,
            day_str,
        )
        file_name = f"{date_obj.year}_{month_str}_{day_str}.csv"
        full_path = os.path.join(data_dir_path, file_name)
        return full_path

    def remove_directory(self, file_path):
        """removes directory with file contents"""
        dir_name = os.path.dirname(file_path)
        shutil.rmtree(dir_name)

    def extract_directory_path(self, file_path: str):
        """
        Extract directory path from the full file path
        """
        self.validate_file_path(file_path)
        return os.path.dirname(file_path)

    def make_directories(self, dir_path: str):
        """Make directories"""
        os.makedirs(dir_path, exist_ok=True)

    def make_directories_from_file_path(self, file_path: str):
        """Make directories from file path"""
        self.make_directories(self.extract_directory_path(file_path))

    def validate_file_path(self, file_path: str):
        """Validate file path"""
        if self.string_helper.is_null_or_whitespace(file_path):
            raise ValueError("File path is null or empty")

    def does_file_exist(self, file_path: str):
        """Check if file exists"""
        return os.path.exists(file_path)

    def construct_file_name(self,
                            file_name_prefix: str,
                            start_date: date,
                            end_date: date,
                            extension: str):
        """construct file name"""
        start_date_str = self.date_helper.convert_date_to_yyyy_mm_dd(
            start_date)
        end_date_str = self.date_helper.convert_date_to_yyyy_mm_dd(end_date)

        return f"{file_name_prefix}_{start_date_str}_{end_date_str}.{extension}"

    def get_file_name_from_path(self, file_path: str):
        """extracts filename from path"""
        self.string_helper.validate_null_or_empty(file_path, "file_path")
        return os.path.basename(file_path)

    def write(self, file_path: str, data):
        """write to file"""
        self.make_directories_from_file_path(file_path)
        self.logger.info("Writing data to file path %s", file_path)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(data)
