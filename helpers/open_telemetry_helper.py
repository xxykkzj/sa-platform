"""Open Telemetry Helper
    reference: https://medium.com/humanmanaged/
    quick-start-to-integrating-opentelemetry-with-fastapi-part-1-2be4fec874bc
"""
import logging
import os
from enum import Enum
from typing import Callable, Sequence
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler, LogData, LogRecord
from opentelemetry.sdk._logs.export import SimpleLogRecordProcessor, ConsoleLogExporter, LogExporter
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry._logs import (
    set_logger_provider
)
from dotenv import load_dotenv
from helpers.date_helper import DateHelper
from helpers.jsonl_helper import JsonlHelper
from helpers.log_helper import log_error
from settings.log_settings import LogSettings

load_dotenv()

logger = logging.getLogger(LogSettings.NAME)


class LogExportResult(Enum):
    """Log Export Result"""
    SUCCESS = 0
    FAILURE = 1


class FileLogExporter(LogExporter):
    """Implementation of :class:`LogExporter` that prints log records to the
    console.

    This class can be used for diagnostic purposes. It prints the exported
    log records to the console STDOUT.
    """

    def __init__(
        self,
        formatter: Callable[[LogRecord], str] = lambda record: record.to_json()
        + os.linesep,
    ):
        self.formatter = formatter
        self.jsonl_helper = JsonlHelper()
        self.date_helper = DateHelper()
        today = self.date_helper.convert_date_to_yyyy_mm_dd(
            self.date_helper.get_utc_now())
        file_name = f"{today}-otel.jsonl"
        self.file_path = os.path.join(".", "logs", "opentelemetry", file_name)

    # pylint: disable=broad-exception-caught
    def export(self, batch: Sequence[LogData]):
        """Export the data"""
        for data in batch:
            try:
                data_to_log = self.formatter(data.log_record)
                self.jsonl_helper.write_jsonlines(self.file_path, data_to_log)
            except Exception as e:
                log_error(logger, "FileLogExporter.export", e)
        return LogExportResult.SUCCESS

    # pylint: enable=broad-exception-caught

    def shutdown(self):
        """shutdown"""

# pylint: disable=too-few-public-methods


class OpenTelemetryHelper():
    """Open Telemetry Helper"""

    def get_log_handler(self):
        """Initialise logging"""
        logger_provider = LoggerProvider(
            resource=Resource.create({})
        )
        set_logger_provider(logger_provider)
        logger_provider.add_log_record_processor(
            SimpleLogRecordProcessor(ConsoleLogExporter()))

        logger_provider.add_log_record_processor(
            SimpleLogRecordProcessor(FileLogExporter()))

        otel_log_handler = LoggingHandler(logger_provider=logger_provider)
        LoggingInstrumentor().instrument(set_logging_format=True)
        return otel_log_handler

# pylint: enable=too-few-public-methods
