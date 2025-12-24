import logging
from datetime import datetime

from mongoengine.errors import DoesNotExist

from backend.application.dto.user_info import UserInfo
from backend.infra.entity.user import User
from backend.infra.exception.errorcode import ErrorCode
from backend.infra.exception.exception import BizException as BE
from backend.infra.util import smtp_util
from backend.infra.util.password_util import md5_encrypt
from backend.infra.util.req_util import get_param


def register(data):
    # 提取参数
    email = get_param("email", data)
    verify_code = get_param("verify_code", data)
    name = get_param("username", data)
    pwd = get_param("password", data)

    # # 验证重复注册
    # try:
    #     user = User.objects.get(email=email)
    #     if user:
    #         raise BE.error(ErrorCode.EMAIL_ALREADY_REGISTERED)
    # except DoesNotExist:
    #     # 没找到是正常情况，继续注册流程
    #     pass
    # except Exception as e:
    #     logging.error(e)
    #     raise e

    # 校验验证码
    check = smtp_util.check_verify_code(email, verify_code)
    if not check:
        raise BE.error(ErrorCode.INVALID_CODE)

    encry_pwd = md5_encrypt(pwd)  # 加密密码

    # 创建用户
    try:
        user = User(
            email=email,
            user_name=name,  # 注意：这里应该是user_name，而不是verify_code
            pwd=encry_pwd,
            created_at=datetime.now()
        )
        user.save()
        return UserInfo(user)
    except Exception as e:
        logging.error(e)
        raise BE.error(ErrorCode.REGISTER_FAILED)


def login(data):
    # 提取参数
    email = get_param('email', data)

    # 查询用户
    try:
        user = User.objects.get(email=email)
    except DoesNotExist:
        raise BE.error(ErrorCode.USER_NOT_FOUND)
    except Exception as e:
        logging.error(e)
        raise e

    # 验证码登录
    if data["verify_code"]:
        # 校验验证码
        verify_code = get_param("verify_code", data)
        check = smtp_util.check_verify_code(email, verify_code)
        if not check:  # 验证失败
            raise BE.error(ErrorCode.INVALID_CODE)

    # 密码登录
    elif data["password"]:
        # md5加密处理
        password = get_param("password", data)
        en_password = md5_encrypt(password)
        # 校验密码
        if user.pwd != en_password:
            raise BE.error(ErrorCode.INVALID_PASSWORD)

    else:
        raise BE.error(ErrorCode.INVALID_PARAMETER)

    return UserInfo(user)


def send_verify_code(data):
    em = get_param("email", data)
    # 发送验证码并存储
    code = smtp_util.send_verify_code(em)
    if not code:  # 默认5分钟内有效
        raise BE.error(ErrorCode.VERIFY_CODE_SEND_FAILED)
