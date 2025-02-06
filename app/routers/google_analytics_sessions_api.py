"""
Google analytics api for sessions data
"""
from datetime import date
import logging
from fastapi import APIRouter
from app.api_helper import get_file_response, get_success_json_response
from google_analytics_module.services.google_analytics_service import GoogleAnalyticsService

router = APIRouter(
    prefix="/google-analytics/sessions",
    tags=["google-analytics-session"],
    # Enable the dependency when you add authentication
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not Found"}})

logger = logging.getLogger(__name__)


def log_request(method_name: str,
                start_date: date,
                end_date: date,
                dataset_id: str = "",
                organisation_id: str = ""):
    """log request params"""
    logger.info("received request for %s.\
                 dataset_id: %s, start_date: %s, end_date: %s, organisation_id %s",
                method_name, dataset_id, start_date, end_date, organisation_id)


@router.get("/dimensions/landing-page/dataset/{dataset_id}")
async def get_by_landing_page_filtered_by_dataset_id(dataset_id: str,
                                                     start_date: date,
                                                     end_date: date):
    """API to return sessions by landing page for a dataset id"""
    log_request("get_by_landing_page_filtered_by_dataset_id", start_date,
                end_date, dataset_id=dataset_id)
    sessions = GoogleAnalyticsService().get_sessions_by_landing_page(
        dataset_id, start_date, end_date)
    return get_success_json_response(sessions)


@router.get("/dimensions/landing-page/organisation/{organisation_id}")
async def get_by_landing_page_filtered_by_organisation_id(organisation_id: str,
                                                          start_date: date,
                                                          end_date: date):
    """get sessions by landing page based on organisation id"""
    log_request("get_by_landing_page_filtered_by_organisation_id", start_date,
                end_date, organisation_id=organisation_id)
    sessions = GoogleAnalyticsService().get_sessions_by_organisation_id(
        start_date, end_date, organisation_id)
    return get_success_json_response(sessions)


@router.get("/dimensions/age/dataset/{dataset_id}")
async def get_by_age_filtered_by_dataset_id(dataset_id: str, start_date: date, end_date: date):
    """API to return sessions by age for a dataset id"""
    log_request("get_by_age_filtered_by_dataset_id", start_date,
                end_date, dataset_id=dataset_id)
    sessions = GoogleAnalyticsService().get_sessions_by_age(
        dataset_id, start_date, end_date)
    return get_success_json_response(sessions)


@router.get("/dimensions/gender/dataset/{dataset_id}")
async def get_by_gender_filtered_by_dataset_id(dataset_id: str, start_date: date, end_date: date):
    """API to return sessions by gender for a dataset id"""
    log_request("get_by_gender_filtered_by_dataset_id", start_date,
                end_date, dataset_id=dataset_id)
    sessions = GoogleAnalyticsService().get_sessions_by_gender(
        dataset_id, start_date, end_date)
    return get_success_json_response(sessions)


@router.get("/dimensions/source/dataset/{dataset_id}")
async def get_by_source_filtered_by_dataset_id(dataset_id: str, start_date: date, end_date: date):
    """API to return sessions by source for a dataset id"""
    log_request("get_by_source_filtered_by_dataset_id", start_date,
                end_date, dataset_id=dataset_id)
    sessions = GoogleAnalyticsService().get_sessions_by_source(
        dataset_id, start_date, end_date)
    return get_success_json_response(sessions)


@router.get("/dimensions/medium/dataset/{dataset_id}")
async def get_by_medium_filtered_by_dataset_id(dataset_id: str, start_date: date, end_date: date):
    """API to return sessions by medium for a dataset id"""
    log_request("get_by_medium_filtered_by_dataset_id", start_date,
                end_date, dataset_id=dataset_id)
    sessions = GoogleAnalyticsService().get_sessions_by_medium(
        dataset_id, start_date, end_date)
    return get_success_json_response(sessions)


@router.get("/dimensions/excel/dataset_url")
async def get_sessions_excel_data_from_dataset_url(dataset_url: str,
                                             start_date: date,
                                             end_date: date):
    """API to return sessions sessions data for all categories"""
    export_file_path = GoogleAnalyticsService().get_sessions_data_as_excel_from_dataset_url(
        dataset_url, start_date, end_date)
    return get_file_response(export_file_path)
