"""Scrape council name"""

import asyncio
import re
import logging
from threading import Semaphore, Thread
from requests.utils import quote
import requests
from bs4 import BeautifulSoup
from joblib import Parallel, delayed
from dtos.cu_dataset_dto import CuDataSetDto
from dtos.get_data_from_url_request_dto import GetDataFromUrlRequestDto
from enums.job_run_status import JobRunStatus
from helpers.date_helper import DateHelper
from helpers.file_helper import FileHelper
from helpers.jsonl_helper import JsonlHelper
from helpers.log_helper import log_error
from helpers.string_helper import StringHelper
from repositories.council_name_repository import CouncilNameRepository
from repositories.job_run_repository import JobRunRepository
from repositories.models.council_name_model import CouncilNameModel
from scraping.find_council_by_address_response import FindCouncilByAddressResponse
from services.web_scraping_service import WebScrapingService
from services.cu_dataset_service import CuDataSetService
from settings.lga_settings import LgaSettings
from settings.log_settings import LogSettings
from settings.sa_community_settings import SaCommunitySettings
from settings.scraping_settings import ScrapingSettings


# pylint: disable=too-many-instance-attributes


class CouncilNameScrapingService:
    """Scrape council name"""

    def __init__(self) -> None:
        self.logger = logging.getLogger(LogSettings.NAME)
        self.string_helper = StringHelper()
        self.file_helper = FileHelper()
        self.web_scraping = WebScrapingService()
        self.cu_dataset_service = CuDataSetService()
        self.jsonl_helper = JsonlHelper()
        self.date_helper = DateHelper()
        self.sacommunity_settings = SaCommunitySettings()
        self.council_name_repository = CouncilNameRepository()
        self.job_run_repository = JobRunRepository()

    def extract_value_replacing_prefix(self, text_array, prefix):
        """
        Extract only the value by removing the prefix
        """
        values = [t for t in text_array if t.startswith(prefix)]
        if len(values) > 0:
            return values[0].replace(prefix, "").strip()

        return ""

    # pylint: disable=broad-exception-caught
    async def find_council_by_address(
        self, address: str, timeout_in_seconds=120, is_headless=True
    ) -> FindCouncilByAddressResponse:
        """
        Finds council by address
        address: address where organization is located
        timeout_in_seconds: timeout in seconds until which the program will
        wait before returning None
        is_headless: if False, a chrome browser will popup,
        else the operation will be done in background
        """
        self.string_helper.validate_null_or_empty(address, "address")

        error_message = ""
        has_error = False
        council_name = ""
        electoral_ward = ""
        text = ""
        try:
            base_url = "https://lga-sa.maps.arcgis.com/apps/instant/lookup/index.html"
            url = f"{base_url}?appid={LgaSettings.APP_ID}&find={quote(address)}"
            self.logger.info("Fetching council for %s", address)
            request_dto = GetDataFromUrlRequestDto(
                url,
                is_headless,
                LgaSettings.TEXT_TO_EXCLUDE,
                timeout_in_seconds,
                LgaSettings.CONTENT_XPATH,
                LgaSettings.NO_RESULT_XPATH,
            )
            text = await self.web_scraping.get_data_from_url_using_playwright_async(request_dto)
            # text = self.web_scraping.get_data_from_url(request_dto)

            if not self.string_helper.is_null_or_whitespace(text):
                text_array = text.splitlines()

                council_name = self.extract_value_replacing_prefix(
                    text_array, "Council Name"
                )
                electoral_ward = self.extract_value_replacing_prefix(
                    text_array, "Electoral Ward"
                )

        except Exception as ex:
            has_error = True
            error_message = str(ex)
            log_error(self.logger, "find_council_by_address", ex)

        return FindCouncilByAddressResponse(
            address, council_name, electoral_ward, text, has_error, error_message
        )

    # pylint: enable=broad-exception-caught

    def find_councils_by_addresses(
        self, addresses: list, is_headless=True, timeout_in_seconds=600
    ):
        """
        Find councils by addresses in parallel
        Example:
        # with less timeout, to check test timeout feature.
        # Without timeout, there is possibility of infinite loop
        # print(find_council_by_address("130 L'Estrange Street, Glenunga", 2))

        # with default timeout, this generally gives data
        # print('council details ', find_council_by_address("130 L'Estrange Street, Glenunga"))
        """
        # maximum number of concurrent requests at a time
        semaphore = Semaphore(
            ScrapingSettings.MAX_CONCURRENT_REQUESTS
        )

        threads = []

        async def find_council(address, all_councils):
            with semaphore:
                try:
                    council = await self.find_council_by_address(
                        address, timeout_in_seconds, is_headless
                    )
                    all_councils.append(council)
                except Exception as ex:
                    # simply log the exception, don't raise it further
                    log_error(self.logger, "find_council", ex)
                    raise ex

        all_councils = []
        for address in addresses:
            thread = Thread(target=find_council, args=(address, all_councils))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return all_councils

    def find_address_from_sacommunity_website(
        self, url: str, is_headless=True, timeout_in_seconds=600
    ):
        """
        Find address from sa community website
        """
        xpath = (
            '//*[@id="content-area"]/div/div[1]/div[2]/div[2]/div/div[1]/div[1]/div[2]'
        )
        return self.web_scraping.get_data_from_url(
            GetDataFromUrlRequestDto(
                url, is_headless, [], timeout_in_seconds, xpath, ""
            )
        )

    # getting council name from sacommunity website based on xpath is not achievable,
    # because the xpath differs based on the contents
    # As the time of this writing, this urls
    # https://sacommunity.org/org/208832-Burnside_Youth_Club and
    # https://sacommunity.org/org/196519-Sturt_Badminton_Club_Inc. has xpath of
    # //*[@id="content-area"]/div/div[4]
    # //*[@id="content-area"]/div/div[5]
    # So it's okay for now to get the council name based on regular expression,
    # thus used beautiful soup
    # test function, useful while debugging
    # url = 'https://sacommunity.org/org/208832-Burnside_Youth_Club'
    # find_address_in_sacommunity(url, False)
    def get_council_from_sacommunity_website(self, url):
        """
        Get council from sacommunity website
        """
        url_response = requests.get(
            url, timeout=ScrapingSettings.TIMEOUT_IN_SECONDS)
        soup = BeautifulSoup(url_response.content)
        council_identifier = "Council:"
        council_text = soup.find("div", string=re.compile(council_identifier))
        council_name = ""
        if council_text is not None:
            council_text = str(council_text)
            start_index = council_text.index(council_identifier)
            council_name = (
                council_text[start_index:]
                .replace(council_identifier, "")
                .replace("</div>", "")
                .strip()
            )

        return council_name

    def find_addresses_from_sacommunity_website(
        self, urls: list, is_headless=True, timeout_in_seconds=600
    ):
        """
        Retrieves addresses from the sa-community website for given lists of urls in parallel
        """
        semaphore = Semaphore(ScrapingSettings.MAX_CONCURRENT_REQUESTS)

        threads = []

        def find_addr(url, all_address):
            with semaphore:
                try:
                    addr = self.find_address_from_sacommunity_website(
                        url, is_headless, timeout_in_seconds
                    )
                    council = self.get_council_from_sacommunity_website(url)
                    all_address.append(
                        {
                            "url": url,
                            "address": addr,
                            "council_in_sacommunity_website": council,
                        }
                    )
                except Exception as ex:
                    log_error(self.logger, "find_addr", ex)
                    raise ex

        all_address = []
        for url in urls:
            thread = Thread(target=find_addr, args=(url, all_address))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return all_address

    def scrape_council_name_based_on_cu_dataset(self,
                                                row_counter,
                                                total,
                                                cu_dataset_dto: CuDataSetDto,
                                                job_run_id):
        """scrape council name from cu_dataset. runs async func in sync func"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.scrape_council_name_based_on_cu_dataset_async(
            row_counter,
            total,
            cu_dataset_dto,
            job_run_id))
        loop.close()

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments
    async def scrape_council_name_based_on_cu_dataset_async(
        self,
        row_counter,
        total,
        cu_dataset_dto: CuDataSetDto,
        job_run_id
    ):
        """
        Scrape council name based on cu export dataframe
        """
        existing_record = self.council_name_repository.get_council_scraped_by_address(
            cu_dataset_dto.get_address())
        log_msg_parts = [f"org: {cu_dataset_dto.organisation_id}, ",
                         f"address: {cu_dataset_dto.get_address()}, ",
                         f"row {row_counter + 1} of {total}."]
        log_msg = "".join(log_msg_parts)
        created_at_unix = None
        council_scraped = ""
        has_error = False
        error_message = ""
        if existing_record:
            self.logger.info("Record exists, so skip %s", log_msg)
            created_at_unix = existing_record.created_at_unix
            council_scraped = existing_record.council_scraped
        else:
            self.logger.info("Scraping %s", log_msg)
            created_at_unix = self.date_helper.get_unix_timestamp()
            if self.string_helper.is_null_or_whitespace(cu_dataset_dto.get_address()):
                error_message = "address is null or empty"
            else:
                council_by_address_response = await self.find_council_by_address(
                    cu_dataset_dto.get_address()
                )
                error_message = council_by_address_response.error_message
                council_scraped = council_by_address_response.council_name
                has_error = council_by_address_response.has_error

        council_name_model = CouncilNameModel(
            job_run_id=job_run_id,
            org_id=cu_dataset_dto.organisation_id,
            org_url=self.sacommunity_settings.get_organisation_url(
                cu_dataset_dto.organisation_id),
            address=cu_dataset_dto.get_address(),
            council=cu_dataset_dto.council,
            council_scraped=council_scraped,
            is_council_matched=cu_dataset_dto.council == council_scraped,
            created_at_unix=created_at_unix,
            has_error=has_error,
            error_message=error_message
        )

        self.council_name_repository.add(council_name_model)

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments

    def get_output_records_organisations(self, output_file_path):
        """
        extract organisation ids
        """
        output_records = self.jsonl_helper.read_jsonlines_all(output_file_path)
        return [o.get("org_id") for o in output_records]

    # def scrape_council_from_dataset_url(self, dataset_url: str, job_run_id, n_jobs=1):

    def scrape_council_from_dataset_url(self, dataset_url: str, job_run_id, n_jobs=3):
        """Scrape council names from dataset url"""
        cu_dataset_dtos = self.cu_dataset_service.read_cu_dataset_from_url(
            dataset_url)

        total = len(cu_dataset_dtos)

        self.job_run_repository.update_status(
            job_run_id, JobRunStatus.IN_PROGRESS)

        Parallel(n_jobs=n_jobs, backend="threading")(
            delayed(self.scrape_council_name_based_on_cu_dataset)(
                row_counter, total, cu_dataset_dto, job_run_id
            )
            for row_counter, cu_dataset_dto in enumerate(cu_dataset_dtos)
        )

        self.job_run_repository.update_status(job_run_id, JobRunStatus.SUCCESS)

    def do_council_scraping_output_require_retry(self, output):
        """
        Check if the retry is required
        """
        # No Results found
        if output.get("scraped_text").startswith("No results found."):
            return True

        # Exceptions
        if output.get(
            "has_error", False
        ) and not self.string_helper.is_null_or_whitespace(output.get("address")):
            return True

        return False

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments
    async def retry_failed_scraping_of_council_name(
        self,
        output_record,
        new_output_file_path: str,
        existing_records,
        row_counter,
        total,
    ):
        """
        Retry scraping
        """
        existing_record = output_record.get("org_id") in existing_records
        if existing_record:
            return

        if self.do_council_scraping_output_require_retry(output_record):
            self.logger.info('Scraping council for org %s address %s. Progress %s of %s',
                             output_record.get("org_id"),
                             output_record.get("address"),
                             row_counter + 1,
                             total,
                             )
            response = await self.find_council_by_address(
                output_record.get("address"))
            output_record["error_message"] = response.error_message
            output_record["has_error"] = response.has_error
            output_record["council_scraped"] = response.council_name
            output_record["electorate_state_scraped"] = response.electoral_ward
            output_record["is_council_correct"] = (
                output_record["council"] == response.council_name
            )
            output_record["scraped_text"] = response.text

        self.jsonl_helper.write_jsonlines(new_output_file_path, output_record)

    # pylint: enable=too-many-arguments
    # pylint: enable=too-many-positional-arguments

    def retry_failed_scraping_of_council_names(
        self, output_file_path: str, new_output_file_path: str, n_jobs=3
    ):
        """
        Retry Failed scraping jobs for council names
        """
        output_records = self.jsonl_helper.read_jsonlines_all(output_file_path)

        total = len(output_records)
        existing_records = []
        if self.file_helper.does_file_exist(new_output_file_path):
            existing_records = self.get_output_records_organisations(
                new_output_file_path
            )
        Parallel(n_jobs=n_jobs)(
            delayed(self.retry_failed_scraping_of_council_name)(
                output_record,
                new_output_file_path,
                existing_records,
                row_counter,
                total,
            )
            for row_counter, output_record in enumerate(output_records)
        )

# pylint: enable=too-many-instance-attributes
