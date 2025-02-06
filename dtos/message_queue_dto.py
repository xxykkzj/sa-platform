"""Message Queue Dto"""
from dataclasses import dataclass


@dataclass
class MessageQueueDto():
    """Message Queue Dto"""
    request_id: str
    message_queue_type: int
    message: any

    def from_dict(self, dict_obj: dict):
        """convert to message queue dto from dict object"""
        return MessageQueueDto(
            request_id=dict_obj.get("request_id"),
            message_queue_type=dict_obj.get("message_queue_type"),
            message=dict_obj.get("message")
        )
