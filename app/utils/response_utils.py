from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Any, Union

def create_response(data: Union[BaseModel, dict, list]) -> JSONResponse:
    """
    格式化 API 回應，支援 Pydantic model、dict、list。
    """
    if isinstance(data, BaseModel):
        data = data.dict()  
    return JSONResponse(content={"status": "success", "data": data})


# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
# from typing import Union

# def success_response(data: Union[BaseModel, dict, list]) -> JSONResponse:
#     if isinstance(data, BaseModel):
#         data = data.dict()
#     return JSONResponse(content={"status": "success", "data": data})

# def error_response(message: str, status_code: int = 400) -> JSONResponse:
#     return JSONResponse(
#         status_code=status_code,
#         content={"status": "error", "message": message}
#     )