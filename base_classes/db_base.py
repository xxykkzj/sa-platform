"""Database base module"""
import logging
from enum import Enum
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database
from helpers.date_helper import DateHelper
from helpers.log_helper import log_error
from settings.database_settings import DatabaseSettings
from settings.log_settings import LogSettings


class DbOperation(Enum):
    """Db opertaion enum"""
    NONE = 0
    ADD = 1
    UPDATE = 2
    SELECT = 3
    SELECT_FIRST = 4


class DbBase():
    """Db base class"""

    def __init__(self) -> None:
        self.logger = logging.getLogger(LogSettings.NAME)
        self.engine = create_engine(DatabaseSettings.DB_URL, echo=True)
        self.date_helper = DateHelper()

    def create_db_if_not_exists(self):
        """create db if not exists"""
        if not database_exists(self.engine.url):
            self.logger.info("Started creating Database")
            create_database(self.engine.url)
            self.logger.info("Completed creating database")

    # pylint: disable=broad-exception-caught
    # pylint: disable=unnecessary-comprehension

    def perform_db_action(self,
                          db_operation: DbOperation,
                          item=None,
                          statement=None):
        """perform db action"""
        with Session(self.engine) as session:
            try:
                if db_operation == DbOperation.ADD:
                    session.add(item)
                elif db_operation == DbOperation.UPDATE:
                    session.execute(statement, item)
                elif db_operation == DbOperation.SELECT:
                    results = session.execute(statement)
                    return [r for r in results]
                elif db_operation == DbOperation.SELECT_FIRST:
                    # return session.execute(statement).scalars().first()
                    return session.execute(statement).first()
                else:
                    raise ValueError(
                        f"Unsupported db operation {db_operation.name}")

                session.commit()

                if db_operation == DbOperation.ADD:
                    return item.id

                return None
            except Exception as ex:
                log_error(self.logger, "update_item", ex)
                session.rollback()
                raise

    # pylint: enable=broad-exception-caught
    # pylint: enable=unnecessary-comprehension

    def add(self, item):
        """add item"""
        return self.perform_db_action(db_operation=DbOperation.ADD, item=item)

    def update_item(self, statement, item):
        """update item"""
        self.perform_db_action(
            db_operation=DbOperation.UPDATE,
            item=item,
            statement=statement)

    def select_item(self, statement):
        """select item"""
        return self.perform_db_action(DbOperation.SELECT, statement=statement)

    def select_first_item(self, statement):
        """select first item"""
        return self.perform_db_action(DbOperation.SELECT_FIRST, statement=statement)

    def delete_item(self, statement):
        """Delete record"""
        delete_data = {
            "is_deleted": True,
            "deleted_at_unix": self.date_helper.get_unix_timestamp()
        }
        self.update_item(statement, delete_data)
