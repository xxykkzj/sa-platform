"""scraping repository module"""

from http import HTTPStatus
from sqlalchemy import select
from base_classes.db_base import DbBase
from helpers.date_helper import DateHelper
from repositories.models.scraping_model import ScrapingModel


class ScrapingRepository(DbBase):
    """Scraping repository class"""

    def __init__(self) -> None:
        super().__init__()
        ScrapingModel.metadata.create_all(self.engine)
        self.date_helper = DateHelper()

    # pylint: disable=singleton-comparison
    def get_failed(self, job_run_id: int):
        """Get job run failed"""
        statement = select(ScrapingModel.request_url,
                           ScrapingModel.response_code,
                           ScrapingModel.error_message).where(
            ScrapingModel.job_run_id == job_run_id).where(
            ScrapingModel.is_deleted == False).where(
            ScrapingModel.response_code != HTTPStatus.OK.value)

        scraping_models = self.select_item(statement)
        return self.convert_to_scraping_model(scraping_models)

    # pylint: enable=singleton-comparison

    def convert_to_scraping_model(self, scraping_models: list[ScrapingModel]):
        """Convert to return models"""
        if not scraping_models:
            return []

        results = []
        for scraping_model in scraping_models:
            results.append({
                "base_url": scraping_model[0],
                "request_url": scraping_model[1],
                "response_code": scraping_model[2],
                "error_message": scraping_model[3]
            })

        return results

    def get_id_by_url(self, url: str, buffer_days=7):
        """Get id for previous url scraping"""
        created_at_unix = self.date_helper.get_previous_day_in_unix(
            buffer_days)
        statement = select(ScrapingModel.id).where(
            ScrapingModel.request_url == url
        ).where(
            ScrapingModel.created_at_unix >= created_at_unix
        ).where(
            ScrapingModel.response_code == HTTPStatus.OK.value
        )

        id_row = self.select_first_item(statement)
        if not id_row:
            return id_row

        return id_row[0]
