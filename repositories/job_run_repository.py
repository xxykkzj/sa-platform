"""Job Run Repository"""

from sqlalchemy import select, update
from base_classes.db_base import DbBase
from enums.job_run_status import JobRunStatus
from enums.job_type import JobType
from exceptions.job_run_not_completed import JobRunNotCompletedException
from exceptions.not_found_exception import NotFoundException
from helpers.date_helper import DateHelper
from helpers.id_helper import IdHelper
from helpers.string_helper import StringHelper
from repositories.models.job_run_model import JobRunModel


class JobRunRepository(DbBase):
    """Job Run repository class"""

    def __init__(self) -> None:
        super().__init__()
        JobRunModel.metadata.create_all(self.engine)
        self.date_helper = DateHelper()
        self.id_helper = IdHelper()
        self.string_helper = StringHelper()

    def add_default(self, job_type: JobType, identifier: str):
        """add default record"""
        job_run_model = JobRunModel(
            created_at_unix=self.date_helper.get_unix_timestamp(),
            job_type_id=job_type.value,
            status_id=JobRunStatus.PENDING.value,
            request_id=self.id_helper.new_id(),
            identifier=identifier
        )
        self.add(job_run_model)
        return job_run_model

    def update_status(self,
                      row_id: int,
                      status: JobRunStatus,
                      error_message=""):
        """Update Status of Job Run"""
        update_status_data = {
            "status_id": status.value,
            "updated_at_unix": self.date_helper.get_unix_timestamp(),
            "error_message": error_message
        }

        update_statement = update(JobRunModel).where(JobRunModel.id == row_id)
        self.update_item(update_statement, update_status_data)

    def delete(self, row_id: int):
        """Delete Job Run"""
        delete_data = {
            "is_deleted": True,
            "deleted_at_unix": self.date_helper.get_unix_timestamp()
        }
        delete_statement = update(JobRunModel).where(JobRunModel.id == row_id)
        self.update_item(delete_statement, delete_data)

    # pylint: disable=singleton-comparison
    def get_by_id(self, row_id: int):
        """Get Job Run by Id"""
        statement = select(JobRunModel.id,
                           JobRunModel.status_id,
                           JobRunModel.job_type_id,
                           JobRunModel.request_id).where(
            JobRunModel.id == row_id).where(
            JobRunModel.is_deleted == False)
        row = self.select_first_item(statement)
        if not row:
            return None

        return JobRunModel(
            id=row[0],
            status_id=row[1],
            job_type_id=row[2],
            request_id=row[3]
        )

    def get_by_status(self, status: JobRunStatus):
        """Get job runs by Status"""
        statement = select(JobRunModel.id, JobRunModel.job_type_id)\
            .where(JobRunModel.status_id == status.value)\
            .where(JobRunModel.is_deleted == False)
        # sqllite needs == False comparision, the linter says to use "not is_deleted"
        rows = self.select_item(statement)
        if not rows:
            return None
        results = []
        for row in rows:
            results.append(JobRunModel(
                id=row[0],
                job_type_id=row[1]
            ))

        return results

    # pylint: enable=singleton-comparison

    def get_by_request_id(self, request_id: str):
        """Get job run by request id"""
        self.string_helper.validate_null_or_empty(request_id, "request_id")
        statement = select(JobRunModel.id, JobRunModel.status_id, JobRunModel.job_type_id).where(
            JobRunModel.request_id == request_id)
        row = self.select_first_item(statement)
        if not row:
            raise NotFoundException(f"request id {request_id} not found")

        return JobRunModel(
            id=row[0],
            status_id=row[1],
            job_type_id=row[2]
        )

    def get_by_request_id_if_completed(self, request_id: str) -> bool:
        """Get job if completed"""
        job_run = self.get_by_request_id(request_id)
        is_completed = job_run.status_id in [
            JobRunStatus.SUCCESS.value, JobRunStatus.FAILED.value]
        if is_completed:
            return job_run

        raise JobRunNotCompletedException(
            f"Job for request_id: {request_id} is not yet completed. Please try again later.")

    def get_all(self):
        """get all job runs"""
        select_statement = select(
            JobRunModel.request_id,
            JobRunModel.created_at_unix,
            JobRunModel.job_type_id,
            JobRunModel.status_id,
            JobRunModel.error_message,
            JobRunModel.id,
            JobRunModel.identifier
        ).order_by(-JobRunModel.id)
        rows = self.select_item(select_statement)
        jobs = []
        for row in rows:
            jobs.append(JobRunModel(
                request_id=row[0],
                created_at_unix=row[1],
                job_type_id=row[2],
                status_id=row[3],
                error_message=row[4],
                id=row[5],
                identifier=row[6],
            ))
        return jobs
