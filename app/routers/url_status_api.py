"""
URL Status API
"""
import os
import logging
from threading import Thread
from fastapi import APIRouter
from app.api_helper import get_success_json_response, \
    prepare_csv_and_return, request_received_response
from enums.job_type import JobType
from enums.message_queue_provider import MessageQueueProvider
from helpers.string_helper import StringHelper
from helpers.url_helper import UrlHelper
from repositories.job_run_repository import JobRunRepository
from repositories.url_status_repository import UrlStatusRepository
from services.url_status_service import UrlStatusService
from settings.app_settings import AppSettings
from settings.file_settings import FileSettings
from settings.log_settings import LogSettings

router = APIRouter(tags=["URL Status"])
logger = logging.getLogger(LogSettings.NAME)


@router.get("/url-status")
async def check_urls_status(url: str):
    """Check url status"""
    logger.info("check_urls_status %s", url)
    response = UrlStatusService().check_urls_status(url)
    return get_success_json_response(response)


@router.get("/url-status-async")
async def check_urls_status_async(url: str):
    """Check url status async"""
    target = UrlStatusService().check_urls_status
    kwargs = {"base_url": url, "update_job_progress": True}
    return check_url_status_from_url_async(url, target, kwargs, JobType.URL_STATUS_CHECKER)


@router.get("/url-status/cu-export-async")
async def check_url_status_cu_export(url: str):
    """Check url status for all organisations in the cu export"""
    target = UrlStatusService().check_urls_for_cu_export_data
    kwargs = {"cu_export_url": url}
    return check_url_status_from_url_async(url, target, kwargs, JobType.URL_STATUS_CHECKER)


def check_url_status_from_url_async(url: str, target, kwargs, job_type):
    """Check url status from url"""
    logger.info("check_urls_status_async %s", url)
    StringHelper().validate_null_or_empty(url, "url")
    # check existing job run
    in_progress_request_id = UrlStatusService().check_if_existing_job_in_progress(url)
    if in_progress_request_id:
        return get_success_json_response(
            {
                "message": "previous job in progress",
                "request_id": in_progress_request_id
            })
    # create a job run
    job_run = JobRunRepository().add_default(job_type, identifier=url)
    if AppSettings.message_queue_provider() == MessageQueueProvider.NONE:
        # create a new thred
        kwargs["job_run_id"] = job_run.id
        Thread(
            target=target,
            daemon=True,
            kwargs=kwargs
        ).start()
    else:
        # call message queue service
        UrlStatusService().add_url_status_to_queue(url, job_run.request_id)

    return request_received_response(job_run.request_id)


@router.get("/url-status/broken-url/{request_id}")
async def get_broken_urls(request_id: str):
    """get broken urls"""
    broken_urls = get_broken_urls_by_request_id(request_id)
    return get_success_json_response(broken_urls)


@router.get("/url-status/broken-url/{request_id}/csv")
async def get_broken_urls_as_csv(request_id: str):
    """get broken urls as csv"""
    broken_urls = get_broken_urls_by_request_id(request_id)
    file_path = os.path.join(
        FileSettings.URL_STATUS_EXPORT_PATH, f"broken_urls_{request_id}.csv")
    return prepare_csv_and_return(broken_urls, file_path)


def get_broken_urls_by_request_id(request_id: str):
    """get broken urls by request id"""
    StringHelper().validate_null_or_empty(request_id, "request_id")
    job_run = JobRunRepository().get_by_request_id_if_completed(request_id)
    return UrlStatusRepository().get_failed_urls(job_run.id)


@router.get("/url-status/website-async")
async def check_url_status_website_async(url: str):
    """check url status of website"""
    target = UrlStatusService().check_urls_statuses
    kwargs = {
        "base_urls": [url],
        "crawl": True,
        "domain": UrlHelper().get_domain(url),
        "skip_db_check": True
    }
    return check_url_status_from_url_async(url, target, kwargs, JobType.URL_STATUS_WEBSITE)
