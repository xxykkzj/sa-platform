"""
URL Status Service module
"""
import logging
from http import HTTPStatus
from joblib import Parallel, delayed
from dtos.message_queue_dto import MessageQueueDto
from dtos.url_status_dto import UrlStatusDto
from enums.job_run_status import JobRunStatus
from enums.message_queue_type import MessageQueueType
from helpers.date_helper import DateHelper
from helpers.id_helper import IdHelper
from helpers.log_helper import log_error
from helpers.string_helper import StringHelper
from helpers.url_helper import UrlHelper
from repositories.job_run_repository import JobRunRepository
from repositories.models.job_run_model import JobRunModel
from repositories.models.url_status_model import UrlStatusModel
from repositories.scraping_repository import ScrapingRepository
from repositories.url_status_repository import UrlStatusRepository
from scraping.scraping_response import ScrapingResponse
from services.web_scraping_service import WebScrapingService
from services.cu_dataset_service import CuDataSetService
from services.message_queue_service import MessageQueueService
from settings.log_settings import LogSettings
from settings.sa_community_settings import SaCommunitySettings

# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-positional-arguments


class UrlStatusService:
    """
    Url Checker. checks if the url is accessible or the is link broken
    """

    def __init__(self) -> None:
        self.string_helper = StringHelper()
        self.url_helper = UrlHelper()
        self.web_scraping = WebScrapingService()
        self.id_helper = IdHelper()
        self.logger = logging.getLogger(LogSettings.NAME)
        self.message_queue_service = MessageQueueService()
        self.cu_dataset_service = CuDataSetService()
        self.job_run_repository = JobRunRepository()
        self.url_status_repository = UrlStatusRepository()
        self.scraping_repository = ScrapingRepository()
        self.date_helper = DateHelper()

    # pylint: disable=broad-exception-caught
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals

    def check_urls_status(self, base_url: str, job_run_id=0,
                          crawl=False, domain="",
                          skip_db_check=True,
                          update_job_progress=False) -> list[ScrapingResponse]:
        """
        Check url statuses for a single base url
        """
        try:
            self.string_helper.validate_null_or_empty(base_url, "base_url")

            if update_job_progress:
                self.job_run_repository.update_status(
                    job_run_id, JobRunStatus.IN_PROGRESS)

            reference_id = 0
            # this is base url, so skip db check
            scraping_response = self.web_scraping.scrape_url(
                url=base_url,
                job_run_id=job_run_id,
                skip_db_check=skip_db_check,
                reference_id=reference_id)
            scraping_response_dict = scraping_response.__dict__
            scraping_response_dict["base_url"] = base_url
            responses = [scraping_response_dict]

            if job_run_id != 0:
                url_status_model = UrlStatusModel(
                    job_run_id=job_run_id,
                    url=base_url,
                    created_at_unix=self.date_helper.get_unix_timestamp()
                )

                self.url_status_repository.add(url_status_model)
                reference_id = url_status_model.id

            if scraping_response.response_code != HTTPStatus.OK.value:
                return responses

            urls = self.url_helper.find_urls(scraping_response.page_content)

            for url in urls:
                url = self.url_helper.remove_query_params(url)
                response = self.web_scraping.scrape_url(
                    url=url,
                    job_run_id=job_run_id,
                    skip_db_check=False,
                    reference_id=reference_id).__dict__
                response["base_url"] = base_url
                responses.append(response)

                if crawl \
                        and not self.string_helper.is_null_or_whitespace(domain)\
                        and domain in url \
                        and not self.url_status_repository.get_by_url_and_run_id(url, job_run_id):
                    return self.check_urls_status(url, job_run_id, crawl, domain, skip_db_check)

            if update_job_progress:
                self.job_run_repository.update_status(
                    job_run_id, JobRunStatus.SUCCESS)
            return responses
        except Exception as ex:
            log_error(self.logger, "check_urls_status", ex)
            self.job_run_repository.update_status(
                job_run_id,
                JobRunStatus.FAILED,
                error_message=str(ex))
            return [ScrapingResponse(
                url=base_url,
                response_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
                page_content="",
                error_name="Exception",
                error_message=str(ex)
            )]

    # pylint: enable=broad-exception-caught
    # pylint: enable=too-many-arguments
    # pylint: enable=too-many-locals

    def add_url_status_to_queue(self, base_url: str, request_id: str):
        """Check url status async using Message Queue"""
        queue_dto = MessageQueueDto(
            request_id=request_id,
            message_queue_type=MessageQueueType.URL_STATUS.value,
            message=UrlStatusDto(
                request_id=request_id,
                url=base_url,
                status=JobRunStatus.PENDING.value,
                responses=""
            ))
        self.message_queue_service.send_message(queue_dto)

    # pylint: disable=too-many-arguments
    def check_urls_statuses(
        self, base_urls: list[str],
        n_jobs=3, job_run_id=0, crawl=False, domain="", skip_db_check=True
    ) -> list[ScrapingResponse]:
        """
        Check url statuses for multiple urls
        """
        self.job_run_repository.update_status(
            job_run_id, JobRunStatus.IN_PROGRESS)
        responses = Parallel(n_jobs=n_jobs, backend="threading")(
            delayed(self.check_urls_status)(
                base_url, job_run_id, crawl, domain, skip_db_check) for base_url in base_urls
        )
        responses_flat = []
        for response_list in responses:
            responses_flat.extend(response_list)

        # check failed status, if not failed then update it success
        job_run = self.job_run_repository.get_by_id(job_run_id)
        if job_run.status_id != JobRunStatus.FAILED.value:
            self.job_run_repository.update_status(
                job_run_id, JobRunStatus.SUCCESS)
        return responses_flat

    # pylint: enable=too-many-arguments

    def check_urls_for_cu_export_data(self, cu_export_url: str, job_run_id=0):
        """
        Check url response statuses with cu_export file path as input
        """
        cu_export_df = self.cu_dataset_service.read_cu_dataset_as_df_from_url(
            cu_export_url)

        # for debugging only
        # org_ids = [196186, 194813, 196271]
        # cu_export_df = cu_export_df[cu_export_df["ID_19"].isin(org_ids)]

        url_prefix = f"{SaCommunitySettings.SA_COMMUNITY_URL}/org/"
        cu_export_df["url"] = url_prefix + cu_export_df["ID_19"].apply(
            str
        )
        urls = cu_export_df["url"].tolist()
        return self.check_urls_statuses(base_urls=urls, job_run_id=job_run_id)

    def check_if_existing_job_in_progress(self, url: str):
        """Check if previous job is in progress"""
        job_run_id = self.url_status_repository.get_latest_job_run_id_by_url(
            url)
        if not job_run_id:
            return False

        job_run: JobRunModel = self.job_run_repository.get_by_id(job_run_id)
        if job_run.status_id in [JobRunStatus.PENDING.value, JobRunStatus.IN_PROGRESS.value]:
            return job_run.request_id

        return None

# pylint: enable=too-many-instance-attributes
# pylint: enable=too-many-positional-arguments
