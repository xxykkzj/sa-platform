"""
Logging helper methods
"""
import os
import logging
from logging.handlers import TimedRotatingFileHandler

from settings.log_settings import LogSettings


def log_error(logger: logging.Logger, caller_name: str, exception: Exception):
    """
    Logs error with details of exception
    """
    logger.error(f"{caller_name} %s", exception,
                 exc_info=True, stack_info=True)


def get_console_log_handler():
    """Console Log Handler"""
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter(
        '%(asctime)s : %(levelname)s : %(message)s')
    console_handler.setFormatter(console_formatter)

    return console_handler


def get_file_log_handler():
    """File Log Handler"""
    file_handler = TimedRotatingFileHandler(
        filename=os.path.join(LogSettings.BASE_DIRECTORY,
                              LogSettings.FOLDER, LogSettings.FILE_NAME),
        encoding=LogSettings.ENCODING,
        when=LogSettings.ROTATION_TIME,
        backupCount=LogSettings.BACKUP_COUNT)
    log_attributes = ["Level: {levelname}", "Time: {asctime}", "Module: {module}",
                      "ProcessId: {process:d}", "ThreadId: {thread:d}", "LineNo: {lineno}",
                      " Message: {message}"]
    file_log_formatter = logging.Formatter(
        ", ".join(log_attributes), style="{")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_log_formatter)

    return file_handler
