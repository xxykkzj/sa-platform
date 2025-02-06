"""
    Api Response Module
"""


class ApiResponse():
    """Api respones class"""
    # pylint: disable=too-few-public-methods

    def __init__(self,
                 is_okay: bool,
                 data: list[any] = None,
                 error_code: int = 0,
                 error_message="") -> None:
        self.is_okay = is_okay
        self.data = [] if data is None else data
        self.error_code = error_code
        self.error_message = error_message

    # pylint: enable=too-few-public-methods
