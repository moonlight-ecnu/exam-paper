import datetime
import logging

import jwt

from backend.infra.consts.security import JWT_SECRET
from backend.infra.exception.errorcode import ErrorCode
from backend.infra.exception.exception import BizException as be


def create_jwt(payload: dict[str, any], exp_minutes=120) -> str:
    """
    应当遵循最小化payload原则
    """
    payload['exp'] = datetime.datetime.now() + datetime.timedelta(minutes=exp_minutes)
    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
    return token

def verify_jwt(token):
    try:
        # 验证JWT
        decoded_payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        # JWT过期
        raise be.error(ErrorCode.JWT_EXPIRED)
    except jwt.InvalidTokenError:
        # JWT无效
        raise be.error(ErrorCode.JWT_INVALID)
    except Exception as e:
        raise e


def get_id_from_jwt(token)->str:
    payload = verify_jwt(token)
    return payload['id']

if __name__ == '__main__':
    token = create_jwt({"id":"TestUser"})
    print(token)
    try:
        verify_jwt(token)
    except Exception as e:
        logging.error(e)
    else:
        print(f"Username: {get_id_from_jwt(token)}") # success