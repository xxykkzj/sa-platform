"""LGA Constants"""

# pylint: disable=too-few-public-methods


class LgaSettings():
    """LGA related settings"""
    APP_ID = "db6cce7b773746b4a1d4ce544435f9da"
    TEXT_TO_EXCLUDE = ["Results:1", "", "Loading..."]
    CONTENT_XPATH = '//*[@id="resultsPanel"]'
    NO_RESULT_XPATH = '//*[@id="noResults"]/calcite-tip/div/div'

# pylint: enable=too-few-public-methods
