"""Helper methods for API"""
from fastapi.responses import JSONResponse, FileResponse
from app.dtos.api_response import ApiResponse
from helpers.file_helper import FileHelper
from helpers.pandas_helper import PandasHelper


def get_success_json_response(content):
    """Construct Success API response"""
    api_response = ApiResponse(is_okay=True, data=content)
    return JSONResponse(content=api_response.__dict__)


def get_file_response(file_path: str):
    """Construct file response"""
    file_helper = FileHelper()
    if not file_helper.does_file_exist(file_path):
        raise FileNotFoundError("File not found")
    file_name = file_helper.get_file_name_from_path(file_path)
    return FileResponse(path=file_path, filename=file_name)


def prepare_csv_and_return(data, file_path: str):
    """Prepare csv and return"""
    PandasHelper().save_list_to_csv(data, file_path)
    return get_file_response(file_path)


def request_received_response(request_id):
    """return request received response"""
    return get_success_json_response({
        "request_id": request_id,
        "message": "Request received. Please check status from /job_runs/{request_id} endpoint"})
