"""Url Model"""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from repositories.models.db_model_base import DbModelBase

# pylint: disable=too-few-public-methods


class UrlStatusModel(DbModelBase):
    """Url Status Model"""
    __tablename__ = "url_statuses"
    job_run_id: Mapped[int] = mapped_column(ForeignKey("job_runs.id"))
    url: Mapped[str] = mapped_column(nullable=False)
    text_hash: Mapped[float] = mapped_column(nullable=True)
