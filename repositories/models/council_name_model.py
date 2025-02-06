"""Council Name Model"""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from repositories.models.db_model_base import DbModelBase

# pylint: disable=too-few-public-methods


class CouncilNameModel(DbModelBase):
    """Council Name"""
    __tablename__ = "council_names"
    job_run_id: Mapped[int] = mapped_column(ForeignKey("job_runs.id"))
    org_id: Mapped[int] = mapped_column(nullable=True)
    org_url: Mapped[str] = mapped_column(nullable=True)
    address: Mapped[str] = mapped_column(nullable=False)
    council: Mapped[str] = mapped_column(nullable=True)
    council_scraped: Mapped[str] = mapped_column(nullable=True)
    is_council_matched: Mapped[bool] = mapped_column(nullable=True)
    has_error: Mapped[bool] = mapped_column(nullable=True)
    error_message: Mapped[str] = mapped_column(nullable=True)

# pylint: disable=too-few-public-methods
