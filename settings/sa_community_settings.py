"""Constans related to SA Community"""

# pylint: disable=too-few-public-methods


class SaCommunitySettings():
    """SA Community related settings"""
    SA_COMMUNITY_URL = "https://sacommunity.org"

    def get_organisation_url(self, organisation_id: int):
        """construct organisation url"""
        return f"{SaCommunitySettings.SA_COMMUNITY_URL}/org/{organisation_id}"

# pylint: enable=too-few-public-methods
