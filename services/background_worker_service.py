"""Background worker"""
import logging
import time

from enums.message_queue_provider import MessageQueueProvider
from exceptions.max_retry_reached_exception import MaxRetryReachedException
from helpers.log_helper import log_error
from settings.app_settings import AppSettings
from settings.log_settings import LogSettings
from settings.message_queue_settings import MessageQueueSettings

# pylint: disable=too-few-public-methods
# pylint: disable=broad-exception-caught


class BackgroundWorkerService():
    """Background worker class"""

    def __init__(self) -> None:
        self.logger = logging.getLogger(LogSettings.NAME)

    def process_message_queue(self):
        """Process Message Queue"""
        try:
            queue_provider = AppSettings.message_queue_provider()
            exception_count = 0
            while True:
                try:
                    self.logger.info("Fetching from queue")
                    if queue_provider == MessageQueueProvider.NONE:
                        raise ValueError(
                            f"Invalid Message Queue Provider: {queue_provider.name}")

                    exception_count = 0
                    if queue_provider == MessageQueueProvider.SQS:
                        self.logger.info("Fetching new message from AWS SQS")

                    elif queue_provider == MessageQueueProvider.RABBIT_MQ:
                        self.logger.info("Fetching new message from RabbitMq")

                    time.sleep(MessageQueueSettings.WAIT_SECONDS)
                except Exception as ex:
                    # in these exceptions we try again,
                    # catch transiet failures like network connection and try again
                    log_error(
                        self.logger, "process_message_queue (inside while loop)", ex)
                    sleep_time = MessageQueueSettings.WAIT_SECONDS * \
                        MessageQueueSettings.DELAY_ON_EXCEPTION

                    exception_count += 1
                    if exception_count == MessageQueueSettings.MAX_RETRY_COUNT_ON_EXCEPTION:
                        raise MaxRetryReachedException(
                            f"Max retry of {exception_count} reached") from ex
                    self.logger.info(
                        "Waiting %s seconds after exception count %s", sleep_time, exception_count)

                    time.sleep(sleep_time)

        except Exception as ex:
            # Catch all exception, you don't want to crash application with uncaught exception
            # the only way to start the job again is to restart the app
            log_error(self.logger, "process_message_queue", ex)

# pylint: enable=too-few-public-methods
# pylint: enable=broad-exception-caught
