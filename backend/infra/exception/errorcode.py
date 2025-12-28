from enum import Enum


class ErrorCode(Enum):
    # 逻辑错误
    INTERNAL_ERROR = (888, "server logical error")
    # 参数验证相关
    INVALID_PARAMETER = (999, "invalid parameter")

    # 身份验证与权限校验
    JWT_INVALID = (1000, "the JWT is in valid, please log back in")
    JWT_EXPIRED = (1001, "the JWT is expired, please log back in")
    INVALID_CODE = (1002, "the verify code is invalid")

    # 数据库相关
    DB_NOT_FOUND = (2000, "not found, please try again")
    DB_DELETE_FAILED = (2001, "delete failed, please try again")

    # 业务逻辑相关
    REGISTER_FAILED = (3000, "register failed, please try again later")
    USER_NOT_FOUND = (3001, "user not found, please register first")
    EMAIL_ALREADY_REGISTERED = (3002, "email already registered, please use another email")
    INVALID_PASSWORD = (3003, "invalid password, please try again")
    INVALID_REQUEST_TYPE = (3007, "invalid request type, it must be 0 or 1")
    VERIFY_CODE_SEND_FAILED = (3008, "verify code send failed, please try again later")
    REGISTER_REPEAT = (3010, "The email address is already registered")

    GROUP_NOT_FOUND = (4000, "group not found, please register first")
    GROUP_CREATE_FAILED = (4001, "group create failed, please try again later")
    GROUP_INVITATION_FAILED = (4002, "failed to initiate invitation")
    GROUP_NOT_INVITED = (4003, "not invited by the group, please wait for invitation")
    GROUP_NO_MEMBER = (4004, "Group doesn't have this member")

    UPLOAD_FAILED = (5000, "upload file failed, please try again")





    def __init__(self, code, msg):
        self.code = code
        self.msg = msg