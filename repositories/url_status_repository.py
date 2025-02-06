"""Url Status repository"""

from http import HTTPStatus
from sqlalchemy import select, update
from base_classes.db_base import DbBase
from helpers.date_helper import DateHelper
from repositories.models.scraping_model import ScrapingModel
from repositories.models.url_status_model import UrlStatusModel

# pylint: disable=singleton-comparison


class UrlStatusRepository(DbBase):
    """Url Status Repository class"""

    def __init__(self) -> None:
        super().__init__()
        UrlStatusModel.metadata.create_all(self.engine)
        self.date_helper = DateHelper()

    def delete(self, row_id: int):
        """Delete Url Status"""
        delete_statement = update(UrlStatusModel).where(
            UrlStatusModel.id == row_id)
        self.delete_item(delete_statement)

    def get_id_by_url_and_hash(self, url: str, text_hash: int):
        """select by url and hash"""
        statement = select(UrlStatusModel.id).where(UrlStatusModel.url == url).where(
            UrlStatusModel.text_hash == text_hash)
        return self.select_item(statement)

    def get_by_url_and_run_id(self, url: str, job_run_id: int):
        """select by url and job run id"""
        url_run_id_stmt = select(
            UrlStatusModel.id).where(
            UrlStatusModel.url == url).where(
            UrlStatusModel.job_run_id == job_run_id).where(
            UrlStatusModel.is_deleted == False)
        return self.select_first_item(url_run_id_stmt)

    def get_latest_job_run_id_by_url(self, url: str):
        """get latest job run id by url"""
        statement = select(UrlStatusModel.job_run_id).where(
            UrlStatusModel.url == url).order_by(UrlStatusModel.id.desc())
        row = self.select_first_item(statement)
        if not row:
            return None

        return row[0]

    def get_failed_urls(self, job_run_id: int):
        """get failed urls"""
        failed_urls_statement = select(
            UrlStatusModel.url,
            ScrapingModel.request_url,
            ScrapingModel.response_code
        ).join(
            ScrapingModel,
            onclause=UrlStatusModel.id == ScrapingModel.reference_id
        ).where(
            UrlStatusModel.job_run_id == job_run_id
        ).where(ScrapingModel.response_code != HTTPStatus.OK.value)

        url_rows = self.select_item(failed_urls_statement)
        if not url_rows:
            return None

        urls = []
        for row in url_rows:
            urls.append({
                "base_url": row[0],
                "url": row[1],
                "response_code": row[2]
            })

        return urls

# pylint: enable=singleton-comparison
