"""Scraping table"""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from repositories.models.db_model_base import DbModelBase

# pylint: disable=too-few-public-methods


class ScrapingModel(DbModelBase):
    """Scraping model"""
    __tablename__ = "scrapings"
    job_run_id: Mapped[int] = mapped_column(ForeignKey("job_runs.id"))
    reference_id: Mapped[int] = mapped_column(nullable=True)
    request_url: Mapped[str] = mapped_column(nullable=False)
    response_url: Mapped[str] = mapped_column(nullable=False)
    response_code: Mapped[int] = mapped_column(nullable=False)
    error_message: Mapped[str] = mapped_column(nullable=True)

# pylint: enable=too-few-public-methods
