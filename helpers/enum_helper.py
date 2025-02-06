"""enum helper"""

# pylint: disable=too-few-public-methods


class EnumHelper():
    """enum helper class"""

    def convert_from_value(self, value: int, enum_type):
        """convert to enum from value"""
        try:
            return enum_type(value)
        except ValueError:
            # Catch value error, and return none
            return enum_type.NONE
