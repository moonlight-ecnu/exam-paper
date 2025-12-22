from backend.infra.exception.errorcode import ErrorCode
from backend.infra.exception.exception import BizException as be

def get_param(param, data):
    if param not in data:
        raise be.error(ErrorCode.INVALID_PARAMETER)
    return data[param]