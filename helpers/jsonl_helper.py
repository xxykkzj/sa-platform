"""JSONl helpers"""
import jsonlines

from helpers.file_helper import FileHelper


class JsonlHelper():
    """Jsonl helper methods"""

    def __init__(self) -> None:
        self.file_helper = FileHelper()

    def read_jsonlines(self, file_path: str):
        """
        Read from jsonlines file
        """

        with jsonlines.open(file_path) as reader:
            yield from reader

    def read_jsonlines_all(self, file_path: str):
        """
        Read from jsonlines without yield
        """
        lines = []
        for line in self.read_jsonlines(file_path):
            lines.append(line)

        return lines

    def write_jsonlines(self, file_path: str, data_obj):
        """
        Append json to jsonl
        """
        if not self.file_helper.does_file_exist(file_path):
            self.file_helper.make_directories_from_file_path(file_path)

        with jsonlines.open(file_path, "a") as writer:
            writer.write(data_obj)
