"""
Council name API
"""
import logging
from threading import Thread
from fastapi import APIRouter
from app.api_helper import get_success_json_response, request_received_response
from enums.job_type import JobType
from repositories.council_name_repository import CouncilNameRepository
from repositories.job_run_repository import JobRunRepository
from scraping.council_name_scraping_service import CouncilNameScrapingService

router = APIRouter(tags=["council"])
logger = logging.getLogger(__name__)


@router.get("/council")
async def get_council_by_address(address: str):
    """
        get council name by address
    """
    logger.info("get_council_by_address %s", address)
    council_name_service = CouncilNameScrapingService()
    council = await council_name_service.find_council_by_address(address)
    return get_success_json_response([council.__dict__])


@router.get("/council/dataset-url-async")
async def get_council_by_dataset_url_async(dataset_url: str):
    """get council for all addresses in cu_dataset data"""
    logger.info("get_council_by_dataset_url: %s", dataset_url)
    job_run = JobRunRepository().add_default(
        JobType.SCRAPE_COUNCIL, identifier=dataset_url)
    Thread(
        target=CouncilNameScrapingService().scrape_council_from_dataset_url,
        daemon=True,
        kwargs={"dataset_url": dataset_url, "job_run_id": job_run.id}
    ).start()

    return request_received_response(job_run.request_id)

@router.get("/council/mismatch/{request_id}")
async def get_mismatch_council(request_id):
    """get council mismatch data"""
    job_run = JobRunRepository().get_by_request_id_if_completed(request_id)
    mismatch_councils = CouncilNameRepository().get_mismatch(job_run.id)
    return get_success_json_response(mismatch_councils)

@router.get("/council/scraping-errors/{request_id}")
async def get_council_scraping_errors(request_id):
    """get council scraping errors"""
    job_run = JobRunRepository().get_by_request_id_if_completed(request_id)
    council_errors = CouncilNameRepository().get_errors(job_run.id)
    return get_success_json_response(council_errors)
