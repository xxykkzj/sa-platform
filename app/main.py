"""
    Main entry point for API
"""

from http import HTTPStatus
import logging
import logging.handlers
from threading import Thread
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from app.dtos.api_response import ApiResponse
from app.routers import job_runs_api, url_status_api
from exceptions.job_run_not_completed import JobRunNotCompletedException
from exceptions.not_found_exception import NotFoundException
from helpers.file_helper import FileHelper
from helpers.log_helper import get_console_log_handler, get_file_log_handler, log_error
from helpers.open_telemetry_helper import OpenTelemetryHelper
from services.background_worker_service import BackgroundWorkerService
from settings.log_settings import LogSettings
from .routers import google_analytics_sessions_api
from .routers import council_name_api

# load environment variables
load_dotenv()

# create logs folder
FileHelper().make_directories(LogSettings.LOG_FILE_PATH)
app = FastAPI()

# configure routers
app.include_router(google_analytics_sessions_api.router)
app.include_router(council_name_api.router)
app.include_router(url_status_api.router)
app.include_router(job_runs_api.router)

logger = logging.getLogger(LogSettings.NAME)
logger.setLevel(logging.DEBUG)

# log handlers
logger.addHandler(get_console_log_handler())
logger.addHandler(get_file_log_handler())
logger.addHandler(OpenTelemetryHelper().get_log_handler())

logger.info("Starting app")

FastAPIInstrumentor.instrument_app(app)


@app.get("/")
async def root():
    """root home page"""
    return {"message": "SA Community Data Analytics API"}


@app.exception_handler(NotFoundException)
async def exception_handler_not_found(request: Request, ex: NotFoundException):
    """Not found exception"""
    return handle_exception(HTTPStatus.NOT_FOUND, request, ex)


@app.exception_handler(Exception)
async def exception_handler(request: Request, ex: Exception):
    """Global exception handler
    https://fastapi.tiangolo.com/tutorial/handling-errors/
    """
    return handle_exception(HTTPStatus.INTERNAL_SERVER_ERROR, request, ex)


@app.exception_handler(JobRunNotCompletedException)
async def job_run_not_completed_handler(request: Request, ex: Exception):
    """job run not completed"""
    return handle_good_exception(HTTPStatus.ACCEPTED, request, ex)


def handle_good_exception(http_status: HTTPStatus, request: Request, ex: Exception):
    """handle good exception"""
    logger.info("handle_good_exception Request %s", str(request))
    api_response = ApiResponse(
        is_okay=True,
        data={"message": str(ex)})

    return JSONResponse(
        status_code=http_status.value,
        content=api_response.__dict__
    )


def handle_exception(http_status: HTTPStatus, request: Request, ex: Exception):
    """handle exception"""
    logger.error("exception_handler Request %s", str(request))
    log_error(logger, "Exception API", ex)
    api_response = ApiResponse(
        is_okay=False,
        data=[],
        error_code=http_status.value,
        error_message=str(ex))

    return JSONResponse(
        status_code=http_status.value,
        content=api_response.__dict__)

# Start background worker


def start_background_message_queue_worker():
    """Start background message queue worker"""
    thread = Thread(target=BackgroundWorkerService(
    ).process_message_queue, daemon=True)
    logger.info("Starting new background queue worker")
    thread.start()

# start_background_message_queue_worker()
