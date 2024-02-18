import logging
import time
import traceback
from typing import Callable

from fastapi import HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from pydantic import ValidationError

logger = logging.getLogger(__name__)


class StandardResponseRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            time_before = time.time()
            try:
                original_response: Response = await original_route_handler(request)
            except ValidationError as exc:
                tb = traceback.format_tb(exc.__traceback__)
                try:
                    msg = repr(exc)
                except Exception as msgExc:
                    msg = str(msgExc)

                try:
                    error_list = [e for e in exc.errors()]
                except:
                    error_list = []

                response_data = {
                    'failed': True,
                    'result': None,
                    'errors': error_list,
                    'debug': {
                        "msg": msg,
                        "loc": tb[-1],
                        "stack": tb,
                    }
                }
                wrapped_response = JSONResponse(response_data)
                return wrapped_response
            except RequestValidationError as exc:
                detail = {
                    "errors": exc.errors(),
                }
                raise HTTPException(status_code=422, detail=detail)
            except HTTPException as exc:
                raise exc
            except Exception as exc:
                tb = traceback.format_tb(exc.__traceback__)
                try:
                    msg = repr(exc)
                except Exception as msgExc:
                    msg = str(msgExc)

                response_data = {
                    'failed': True,
                    'result': None,
                    'errors': [msg],
                    'debug': {
                        "msg": msg,
                        "loc": tb[-1],
                        "stack": tb,
                    }
                }
                wrapped_response = JSONResponse(response_data)
                return wrapped_response

            duration_ms = 1000.0 * (time.time() - time_before)
            original_response.headers["X-Response-Time-MS"] = str(duration_ms)

            # self.path_format contains the format of the endpoint URL - the definition with "{...}" in place for any
            # path parameter(s). See starlette/routing.py:Route for reference.
            route_format = self.path_format

            http_method = request.method
            route_identifier = f"{http_method} {route_format}"

            return original_response

        return custom_route_handler