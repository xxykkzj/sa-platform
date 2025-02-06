"""Message Queue Service module"""

from dtos.message_queue_dto import MessageQueueDto


class MessageQueueService():
    """An abstraction layer for Message Queue
    Current queue is SQS, but later will add rabbitmq as message queue too.
    """

    def __init__(self, queue_provider=None) -> None:
        self.queue_provider = queue_provider

    def send_message(self, message_queue_dto: MessageQueueDto):
        """Send message to queue"""
        if not self.queue_provider:
            raise ValueError("Queue provider is null")

        self.queue_provider.send_message(message_queue_dto)

    def receive_message(self):
        """Receive message from queue"""
        if not self.queue_provider:
            raise ValueError("Queue provider is null")

        return self.queue_provider.receive_message()
