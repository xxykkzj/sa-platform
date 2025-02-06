"""Job runs api"""

import logging
from fastapi import APIRouter
from app.api_helper import get_success_json_response
from enums.job_run_status import JobRunStatus
from enums.job_type import JobType
from helpers.date_helper import DateHelper
from helpers.enum_helper import EnumHelper
from repositories.job_run_repository import JobRunRepository
from repositories.models.job_run_model import JobRunModel
from settings.log_settings import LogSettings


router = APIRouter(tags=["Job Runs"])
logger = logging.getLogger(LogSettings.NAME)


def convert_job_run(job_run: JobRunModel):
    """convert job run to return"""
    if not job_run:
        return {}
    enum_helper = EnumHelper()
    date_helper = DateHelper()
    return {
        "id": job_run.id,
        "job_type_id": job_run.job_type_id,
        "job_type": enum_helper.convert_from_value(job_run.job_type_id, JobType).name,
        "status_id": job_run.status_id,
        "status": enum_helper.convert_from_value(job_run.status_id, JobRunStatus).name,
        "request_id": job_run.request_id,
        "error_message": job_run.error_message,
        "created_at_unix": job_run.created_at_unix,
        "created_at": str(date_helper.from_unix_seconds_to_date(job_run.created_at_unix)),
        "identifier": job_run.identifier
    }


@router.get("/job-runs/{request_id}")
async def get_job_runs_by_request_id(request_id: str):
    """get job run by request id"""
    job_run = JobRunRepository().get_by_request_id(request_id)
    return get_success_json_response(convert_job_run(job_run))


@router.get("/job-runs")
async def get_job_runs():
    """get all job runs"""
    job_runs = JobRunRepository().get_all()
    job_runs_converted = [convert_job_run(j) for j in job_runs]
    return get_success_json_response(job_runs_converted)
