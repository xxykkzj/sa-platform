"""Base class for db model"""
from sqlalchemy.orm import DeclarativeBase,  Mapped, mapped_column

# pylint: disable=too-few-public-methods


class DbModelBase(DeclarativeBase):
    """Db Model Base"""
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False, index=True)
    created_at_unix: Mapped[int] = mapped_column(nullable=False)
    created_by: Mapped[int] = mapped_column(nullable=True)
    updated_at_unix: Mapped[int] = mapped_column(nullable=True)
    updated_by: Mapped[int] = mapped_column(nullable=True)
    is_deleted: Mapped[bool] = mapped_column(nullable=False, default=False)
    deleted_at_unix: Mapped[int] = mapped_column(nullable=True)
    deleted_by: Mapped[int] = mapped_column(nullable=True)
