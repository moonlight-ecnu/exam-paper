from enum import Enum


class ErrorCode(Enum):
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
    INVALID_PASSWORD = (3002, "invalid password, please enter the correct password")
    AVATAR_UPLOAD_FAILED = (3003, "avatar upload failed, please try again later")
    PASSWORD_UPDATE_FAILED = (3004, "password update failed, please try again later")
    USERNAME_UPDATE_FAILED = (3005, "user update failed, please try again later")
    EMAIL_ALREADY_REGISTERED = (3006, "email already registered, please use another email")
    INVALID_REQUEST_TYPE = (3007, "invalid request type, it must be 0 or 1")
    VERIFY_CODE_SEND_FAILED = (3008, "verify code send failed, please try again later")
    IP_NOT_EXIT = (3009, "user doesn't have ip")
    REGISTER_REPEAT = (3010, "The email address is already registered")
    POINT_UPDATE_FAILED = (3011, "point update failed, please try again later")

    UPLOAD_FAILED = (4000, "upload file failed, please try again")





    def __init__(self, code, msg):
        self.code = code
        self.msg = msg