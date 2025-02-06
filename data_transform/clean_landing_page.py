"""clean landing page"""

import math
import pandas as pd

from settings.sa_community_settings import SaCommunitySettings


class CleanLandingPage:
    """cleans the landing page"""

    def __init__(self) -> None:
        self.sacommunity_url = SaCommunitySettings.SA_COMMUNITY_URL

    def get_organization_id(self, text: str) -> str:
        """get organization id"""
        if "-" in text:
            return int(text[: text.index("-")])
        return None

    def get_organization_name(self, text: str) -> str:
        """get organization name"""
        if "-" in text:
            return text[text.index("-") + 1:]
        return None

    def clean_landing_page_text(self, text: str) -> str:
        """clean landing page"""
        search_cache_identifier = "/search?q=cache:"
        if search_cache_identifier in text:
            text = text[text.index(self.sacommunity_url):].replace(
                self.sacommunity_url, ""
            )

        suffixes_to_remove = ["?fbclid=", "+&", "?_x_tr_", "?back="]
        for suffix_to_remove in suffixes_to_remove:
            if suffix_to_remove in text:
                text = text[: text.index(suffix_to_remove)]

        # remove underscore
        text = text.replace("_", " ")
        # remove /org/
        text = text.replace("/org/", "")

        return text.strip()

    def get_sessions_by_organization(
        self, df_ga_orig: pd.DataFrame, landing_page_column_name: str = "landingPage"
    ) -> pd.DataFrame:
        """get sessions by organization"""
        df_ga = df_ga_orig.dropna().copy()
        df_ga["organization_id_name"] = df_ga[landing_page_column_name].apply(
            self.clean_landing_page_text
        )
        df_ga["organization_id"] = df_ga["organization_id_name"].apply(
            self.get_organization_id
        )
        df_ga["organization_name"] = df_ga["organization_id_name"].apply(
            self.get_organization_name
        )
        return df_ga
        # return df_ga[[landing_page_column_name, "organization_id_name", "organization_id",
        #               "organization_name", "sessions"]]

    def process_data(
        self, landing_page_df, sa_community_df, landing_page_column_name="landingPage"
    ) -> pd.DataFrame:
        """process data"""
        sessions_data_df = self.get_sessions_by_organization(landing_page_df)
        results = []
        for _, row in sessions_data_df.iterrows():
            org_id = row["organization_id"]
            if math.isnan(org_id):
                print("org id is invalid, so skip it ", org_id)
                continue

            if org_id is not None:
                org_id = int(org_id)

            # organization name from sa-community file
            org_names_sa_community = sa_community_df[
                sa_community_df["ID_19"] == org_id
            ]["Org_name"].values
            organization_name_sa_community = ""
            is_record_available_in_sacommunity_db = False
            if len(org_names_sa_community) > 0:
                organization_name_sa_community = org_names_sa_community[0]
                is_record_available_in_sacommunity_db = True

            # organization name from google analytics file
            org_names_google = sessions_data_df[
                sessions_data_df["organization_id"] == org_id
            ]["organization_name"].values

            landing_page = (
                self.sacommunity_url
                + sessions_data_df[sessions_data_df["organization_id"] == org_id][
                    landing_page_column_name
                ].values[0]
            )

            result = {
                "org_id": org_id,
                "landing_page": landing_page,
                "sessions_count": row["sessions"],
                "organization_name_sa_community": organization_name_sa_community,
                "organization_name_google": ""
                if len(org_names_google) == 0
                else org_names_google[0],
                "is_record_available_in_sacommunity_db": is_record_available_in_sacommunity_db,
            }

            for col in sessions_data_df.columns:
                if col not in result:
                    result[col] = row[col]

            results.append(result)

        return pd.DataFrame(results)
