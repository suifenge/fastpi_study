from fastapi import status
from fastapi.responses import JSONResponse, Response
from typing import Union


def response(*, code=0, data: Union[list, dict, str], message='Success') -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': code,
            'success': True,
            'message': message,
            'data': data
        }
    )
