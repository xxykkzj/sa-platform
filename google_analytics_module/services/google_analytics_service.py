"""
Google analytics service
"""

import os
from datetime import date
from joblib import Parallel, delayed
import pandas as pd
from dtos.cu_dataset_dto import CuDataSetDto
from dtos.date_range_dto import DateRangeDto
from google_analytics_module.dtos.google_analytics_filter_clause_dto import (
    GoogleAnalyticsFilterClause,
)
from google_analytics_module.dtos.google_analytics_request_config_dto import (
    GoogleAnalyticsRequestConfig,
)
from google_analytics_module.repositories.google_analytics_repository_v4 import (
    GoogleAnalyticsRepositoryV4,
)
from helpers.date_helper import DateHelper
from helpers.excel_helper import ExcelHelper
from helpers.file_helper import FileHelper
from helpers.id_helper import IdHelper
from helpers.pandas_helper import PandasHelper
from services.cu_dataset_service import CuDataSetService
from settings.file_settings import FileSettings
from settings.google_analytics_settings import GoogleAnalyticsSettings


class GoogleAnalyticsService:
    """Google analytics service"""

    def __init__(self, google_analytics_repository=None) -> None:
        if google_analytics_repository is None:
            self.google_analytics_repository = GoogleAnalyticsRepositoryV4()
        else:
            self.google_analytics_repository = google_analytics_repository
        self.pandas_helper = PandasHelper()
        self.cu_dataset_service = CuDataSetService()
        self.excel_helper = ExcelHelper()
        self.file_helper = FileHelper()
        self.date_helper = DateHelper()
        self.id_helper = IdHelper()

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments

    def get_data(
        self,
        dataset_id: str,
        start_date: date,
        end_date: date,
        dimensions,
        metrics,
        organisation_id: int = 0,
    ):
        """Get data from google analytics"""
        filter_clause = GoogleAnalyticsFilterClause()
        filter_clause.set_dataset_id(dataset_id)
        filter_clause.set_date_range(
            DateRangeDto(start_date=start_date, end_date=end_date)
        )
        filter_clause.set_organisation_id(organisation_id)
        request_config = GoogleAnalyticsRequestConfig(dimensions, metrics)
        results = self.google_analytics_repository.get_data(
            property_id=GoogleAnalyticsSettings.PROPERTY_ID,
            request_config=request_config,
            filter_clause=filter_clause,
        )

        return results

    # pylint: enable=too-many-arguments
    # pylint: enable=too-many-positional-arguments

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments
    def get_sessions_by_landing_page(
        self,
        dataset_id: str,
        start_date: date,
        end_date: date,
        organisation_id: int = 0,
        additional_dimensions: list[str] = None,
        additional_metrics: list[str] = None,
    ):
        """get session data with landing page
        additional dimensions could be "eventName", "date"
        additional metrics could be "eventCount"
        """
        dimensions = ["customEvent:DatasetID", "landingPage"]
        if additional_dimensions:
            dimensions.extend(additional_dimensions)

        metrics = ["sessions"]
        if additional_metrics:
            metrics.extend(additional_metrics)

        return self.get_data(
            dataset_id,
            start_date,
            end_date,
            dimensions,
            metrics,
            organisation_id=organisation_id,
        )

    # pylint: enable=too-many-arguments
    # pylint: enable=too-many-positional-arguments

    def get_sessions_by_landing_page_as_df(
        self,
        dataset_id: str,
        start_date: date,
        end_date: date,
        organisation_id: str = "",
    ):
        """Get sessions by landing page as dataframe"""
        results = self.get_sessions_by_landing_page(
            dataset_id, start_date, end_date, organisation_id=organisation_id
        )
        results_df = pd.DataFrame(results)
        return self.pandas_helper.convert_data_types(results_df)

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments
    def get_sessions_by_organisation_id(
        self,
        start_date: date,
        end_date: date,
        organisation_id: int,
        row_count=None,
        total_count=None,
    ):
        """get sessions by organisation id"""
        if row_count and total_count:
            print(
                f"get_sessions_by_landing_page row_count {row_count}\
                    of {total_count}. organisation_id: {organisation_id}"
            )
        sessions = self.get_sessions_by_landing_page(
            "", start_date, end_date, organisation_id
        )
        sessions_count = 0
        for session in sessions:
            sessions_count += int(session.get("sessions", 0))

        landing_page = "" if len(
            sessions) == 0 else sessions[0].get("landingPage", "")

        return {
            "organisation_id": organisation_id,
            "sessions_count": sessions_count,
            "landing_page": landing_page
        }

    # pylint: enable=too-many-arguments
    # pylint: enable=too-many-positional-arguments

    def get_sessions_by_organisation_ids(
        self, start_date: date, end_date: date, organisation_ids: list[int], n_jobs=5
    ):
        """get sessions by organisation ids"""
        total_count = len(organisation_ids)
        return Parallel(n_jobs=n_jobs)(
            delayed(self.get_sessions_by_organisation_id)(
                start_date, end_date, organisation_id, row_count, total_count
            )
            for row_count, organisation_id in enumerate(organisation_ids)
        )

    def get_sessions_by_organisation_ids_as_df(
        self,
        start_date: date,
        end_date: date,
        organisation_ids: list[str],
        n_jobs=5,
    ):
        """get sessions by organisation ids as dataframe"""
        sessions = self.get_sessions_by_organisation_ids(
            start_date=start_date,
            end_date=end_date,
            organisation_ids=organisation_ids,
            n_jobs=n_jobs,
        )
        return pd.DataFrame(sessions)

    def get_sessions_by_age(self, dataset_id: str, start_date: date, end_date: date):
        """get sessions data by age"""
        dimensions = ["customEvent:DatasetID", "userAgeBracket"]
        metrics = ["sessions"]

        return self.get_data(dataset_id, start_date, end_date, dimensions, metrics)

    def get_sessions_by_age_as_df(
        self, dataset_id: str, start_date: date, end_date: date
    ):
        """get sessions by age as dataframe"""
        results = self.get_sessions_by_age(dataset_id, start_date, end_date)
        return pd.DataFrame(results)

    def get_sessions_by_gender(self, dataset_id: str, start_date: date, end_date: date):
        """get session data by gender"""
        dimensions = ["customEvent:DatasetID", "userGender"]
        metrics = ["sessions"]

        return self.get_data(dataset_id, start_date, end_date, dimensions, metrics)

    def get_sessions_by_gender_as_df(
        self, dataset_id: str, start_date: date, end_date: date
    ):
        """get sessions by gender as dataframe"""
        results = self.get_sessions_by_gender(dataset_id, start_date, end_date)
        return pd.DataFrame(results)

    def get_sessions_by_source(self, dataset_id: str, start_date: date, end_date: date):
        """get session data by source"""
        dimensions = ["customEvent:DatasetID", "sessionSource"]
        metrics = ["sessions"]

        return self.get_data(dataset_id, start_date, end_date, dimensions, metrics)

    def get_sessions_by_source_as_df(
        self, dataset_id: str, start_date: date, end_date: date
    ):
        """get sessions by source as dataframe"""
        results = self.get_sessions_by_source(dataset_id, start_date, end_date)
        return pd.DataFrame(results)

    def get_sessions_by_medium(self, dataset_id: str, start_date: date, end_date: date):
        """get session data by source"""
        dimensions = ["customEvent:DatasetID", "sessionMedium"]
        metrics = ["sessions"]

        return self.get_data(dataset_id, start_date, end_date, dimensions, metrics)

    def get_sessions_by_medium_as_df(
        self, dataset_id: str, start_date: date, end_date: date
    ):
        """get sessions by medium as dataframe"""
        results = self.get_sessions_by_medium(dataset_id, start_date, end_date)
        return pd.DataFrame(results)

    def add_more_features_to_sessions_by_landing_page(self,
                                                      cu_datasets: list[CuDataSetDto],
                                                      sessions: list):
        """add features to session data"""
        for session in sessions:
            organisation_id = session["organisation_id"]
            cu_dataset = [
                c for c in cu_datasets if c.organisation_id == organisation_id][0]
            session["organisation_name"] = cu_dataset.organisation_name
            session["primary_category"] = cu_dataset.primary_category
            session["council"] = cu_dataset.council
            session["electoral_state"] = cu_dataset.electoral_state
            session["electoral_federal"] = cu_dataset.electoral_federal

        return sessions

    def get_sessions_data_as_excel_from_dataset_url(self,
                                                    dataset_url: str,
                                                    start_date: date,
                                                    end_date: date):
        """get sessions data for all categories with input as dataset_url"""
        dataset_id_texts = [s for s in dataset_url.split(
            "&") if s.startswith("d=")]
        if len(dataset_id_texts) == 0:
            raise ValueError("Couldnot extract datasetid from dataset url")

        if len(dataset_id_texts) > 1:
            raise ValueError(f"Only one datasetid is supported. However {
                             len(dataset_id_texts)} received.")

        dataset_id = dataset_id_texts[0].replace("d=", "")

        cu_datasets = self.cu_dataset_service.read_cu_dataset_from_url(
            dataset_url)

        return self.get_sessions_data_as_excel(dataset_id,
                                               cu_datasets,
                                               start_date,
                                               end_date)

    def get_sessions_data_as_excel(self,
                                   dataset_id: str,
                                   cu_datasets: list[CuDataSetDto],
                                   start_date: date,
                                   end_date: date):
        """get sessions data for all categories"""
        organisation_ids = [c.organisation_id for c in cu_datasets]
        created_date_utc_start = self.date_helper.get_utc_now()
        date_in_filename = self.file_helper.get_file_name_based_on_date(
            created_date_utc_start)
        export_file_path = os.path.join(
            FileSettings.EXPORT_EXCEL_ROOT_PATH,
            f"{dataset_id}_{date_in_filename}_{self.id_helper.new_id()}.xlsx")

        sessions_by_landing_page = self.get_sessions_by_organisation_ids(
            start_date, end_date, organisation_ids)

        self.add_more_features_to_sessions_by_landing_page(
            cu_datasets, sessions_by_landing_page)

        self.excel_helper.write_to_excel(
            export_file_path, sessions_by_landing_page, "landing_page")

        session_methods = [
            (self.get_sessions_by_age, "age"),
            (self.get_sessions_by_gender, "gender"),
            (self.get_sessions_by_source, "source"),
            (self.get_sessions_by_medium, "medium")]

        for method, sheet_name in session_methods:
            sessions = method(dataset_id, start_date, end_date)
            self.excel_helper.write_to_excel(
                export_file_path, sessions, sheet_name)

        created_date_utc_end = self.date_helper.get_utc_now()

        self.excel_helper.write_to_excel(
            export_file_path,
            [{
                "dataset_id": dataset_id,
                "report_start_date": start_date,
                "report_end_date": end_date,
                "created_date_utc_start": str(created_date_utc_start),
                "created_date_utc_end": str(created_date_utc_end),
                "elapsed_seconds": self.date_helper.get_elapsed_time_in_seconds(
                    created_date_utc_start, created_date_utc_end)
            }],
            "metadata")

        return export_file_path
