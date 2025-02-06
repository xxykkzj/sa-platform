"""council name repository module"""

from sqlalchemy import select, update
from base_classes.db_base import DbBase
from helpers.date_helper import DateHelper
from repositories.models.council_name_model import CouncilNameModel

# pylint: disable=singleton-comparison


class CouncilNameRepository(DbBase):
    """council name repository"""
    def __init__(self) -> None:
        super().__init__()
        CouncilNameModel.metadata.create_all(self.engine)
        self.date_helper = DateHelper()

    def delete(self, row_id: int):
        """Delete Council name record"""
        delete_statement = update(CouncilNameModel).where(
            CouncilNameModel.id == row_id)
        self.delete_item(delete_statement)

    def get_council_scraped_by_address(self, address: str):
        """get council name record by address"""
        get_by_address_stmt = select(
            CouncilNameModel.id,
            CouncilNameModel.council_scraped,
            CouncilNameModel.created_at_unix
        ).where(
            CouncilNameModel.address == address
        ).where(
            CouncilNameModel.has_error == False
        ).where(
            CouncilNameModel.is_deleted == False
        ).order_by(CouncilNameModel.id.desc())

        council_row = self.select_first_item(get_by_address_stmt)
        if not council_row:
            return None

        return CouncilNameModel(
            id=council_row[0],
            council_scraped=council_row[1],
            created_at_unix=council_row[2]
        )

    def get_errors(self, job_run_id: int):
        """get council scraping errors"""
        return self.get_council_scrapings(
            where_clause=CouncilNameModel.has_error == True,
            job_run_id=job_run_id
        )

    def get_mismatch(self, job_run_id: int):
        """get mismatch council"""
        return self.get_council_scrapings(
            where_clause=CouncilNameModel.is_council_matched == False,
            job_run_id=job_run_id
        )

    def get_council_scrapings(self, where_clause, job_run_id):
        """get council scrapings"""
        council_select_stmt = select(
            CouncilNameModel.org_url,
            CouncilNameModel.address,
            CouncilNameModel.council,
            CouncilNameModel.council_scraped
        ).where(where_clause).where(
            CouncilNameModel.job_run_id == job_run_id
        ).where(CouncilNameModel.is_deleted == False)

        mismatch_rows = self.select_item(council_select_stmt)
        if not mismatch_rows:
            return None

        councils = []
        for row in mismatch_rows:
            councils.append({
                "org_url": row[0],
                "address": row[1],
                "council": row[2],
                "council_scraped": row[3]
            })

        return councils

# pylint: enable=singleton-comparison
