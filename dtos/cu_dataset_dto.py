"""DTO for Cudataset"""
class CuDataSetDto():
    """cu_dataset dto"""

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-few-public-methods
    def __init__(self) -> None:
        self.organisation_id = 0
        self.organisation_name = ""
        self.primary_category = ""
        self.street_address_line_1 = ""
        self.suburb = ""
        self.council = ""
        self.electoral_state = ""
        self.electoral_federal = ""

    def get_address(self):
        """returns address"""
        return f"{self.street_address_line_1}, {self.suburb}"

    # pylint: enable=too-many-instance-attributes
    # pylint: enable=too-few-public-methods
