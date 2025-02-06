"""SQS message DTO"""
from dataclasses import dataclass


@dataclass
class SqsMessageDto():
    """DTO for SQS Message"""
    message_id: str
    body: any
    body_md5: str
    receipt_handle: str
    sent_timestamp_milliseconds: int
    approximate_receive_count: int
