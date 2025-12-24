from flask import Blueprint, request
from backend.application.service import user
from backend.infra.util import resp_util as re
from backend.infra.exception.exception import BizException

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/register', methods=['POST'])
def register():
    """
    用户注册
    注：向用户发送验证码并暂存的逻辑在另一接口
    :param:
        email 邮箱
        verify_code 验证码
        password 密码
        username 昵称
    """
    data = request.get_json()
    try:
        res = user.register(data)
    except BizException as e:
        return re.fail(e)
    return re.succeed(res)



@bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    try:
        res = user.login(data)
    except BizException as e:
        return re.fail(e)
    return re.succeed(res)

@bp.route('/send_verify_code', methods=['POST'])
def send_verify_code():
    """
        发送验证码接口
        :param:
            verify_id: 邮箱
            type: 请求类型 (1-login 2-register)
        :return:
            消息提示
        """
    # 获取请求数据
    data = request.get_json()
    try:
        result = user.send_verify_code(data)
    except BizException as e:
        return re.fail(e)
    return re.succeed(result)