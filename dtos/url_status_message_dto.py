"""Url Status Dto"""
from dataclasses import dataclass


@dataclass
class UrlStatusMessageDto():
    """Url Status Message Dto"""
    url: str

    def from_dict(self, dict_obj: dict):
        """convert to object from dict object"""
        return UrlStatusMessageDto(url=dict_obj.get("url"))
