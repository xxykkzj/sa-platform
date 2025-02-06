"""Url Status Dto"""

from dataclasses import dataclass


@dataclass
class UrlStatusDto():
    """Url Status Dto"""
    request_id: str
    url: str
    status: int
    responses: any
