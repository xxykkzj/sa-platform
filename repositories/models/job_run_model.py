"""Job Run module"""

from sqlalchemy.orm import Mapped, mapped_column
from repositories.models.db_model_base import DbModelBase

# pylint: disable=too-few-public-methods


class JobRunModel(DbModelBase):
    """Job run class"""
    __tablename__ = "job_runs"

    job_type_id: Mapped[int] = mapped_column(nullable=False)
    status_id: Mapped[int] = mapped_column(nullable=False)
    request_id: Mapped[str] = mapped_column(nullable=False, index=True)
    error_message: Mapped[str] = mapped_column(nullable=True)
    identifier: Mapped[str] = mapped_column(nullable=True, index=True)
