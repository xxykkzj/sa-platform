"""cu dataset export module"""
import io
import requests
import pandas as pd
from dtos.cu_dataset_dto import CuDataSetDto
from helpers.url_helper import UrlHelper
from helpers.string_helper import StringHelper


class CuDataSetService():
    """cu export dataset"""

    def __init__(self) -> None:
        self.string_helper = StringHelper()
        self.url_helper = UrlHelper()

    def read_cu_dataset_as_df_from_url(self, url: str, timeout = 200) -> pd.DataFrame:
        """read csv from url"""
        self.string_helper.validate_null_or_empty(url, "url")
        if not self.url_helper.is_valid_url(url):
            raise ValueError(f"Invalid Url: {url}")

        if not url.startswith("https://sacommunity.org/export?p=19&"):
            raise ValueError(f"Invalid export url {url}")

        content = requests.get(url, timeout=timeout).content
        return pd.read_csv(io.StringIO(content.decode("utf-8")))

    def read_cu_dataset_from_url(self, dataset_url: str) -> list[CuDataSetDto]:
        """read cu dataset as dto with input as dataset_url"""
        df = self.read_cu_dataset_as_df_from_url(dataset_url)
        return self.construct_cu_dataset_dtos(df)

    def construct_cu_dataset_dtos(self, df: pd.DataFrame) -> list[CuDataSetDto]:
        """construct dto"""
        # Fill empty string in na
        df['Street_Address_Line_1'].fillna("", inplace=True)
        cu_dataset_dtos = []
        for _, row in df.iterrows():
            cu_dataset = CuDataSetDto()
            cu_dataset.organisation_id = row["ID_19"]
            cu_dataset.organisation_name = row["Org_name"]
            cu_dataset.street_address_line_1 = row["Street_Address_Line_1"]
            cu_dataset.suburb = row["Suburb"]
            cu_dataset.primary_category = row["Primary_Category"]
            cu_dataset.council = row["Organisati_Council"]
            cu_dataset.electoral_state = row["Organisati_Electorate_State_"]
            cu_dataset.electoral_federal = row["Organisati_Electorate_Federal_"]

            cu_dataset_dtos.append(cu_dataset)

        # for debugging
        # return cu_dataset_dtos[0:2]

        return cu_dataset_dtos
