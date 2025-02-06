"""Ids helper module"""
import uuid


class IdHelper():
    """Id Helper"""

    # pylint: disable=too-few-public-methods
    def new_id(self):
        """generates a new uuid4"""
        return str(uuid.uuid4())

    # pylint: enable=too-few-public-methods
