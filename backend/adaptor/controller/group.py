from flask import Blueprint, request

from backend.application.service import group
from backend.infra.exception.exception import BizException
from backend.infra.util import jwt_util
from backend.infra.util import resp_util as re

bp = Blueprint('group', __name__, url_prefix='/group')

@bp.route('/create', methods=['POST'])
def create():
    """
    :param:
        name 小组名
    """
    data = request.get_json()
    uid = jwt_util.get_id_from_jwt(request.headers.get('Authorization'))
    try:
        res = group.create(data, uid)
    except BizException as e:
        return re.fail(e)
    return re.succeed(res)

@bp.route('/dismiss', methods=['POST'])
def dismiss():
    """解散小组"""
    pass

@bp.route('/invite', methods=['POST'])
def invite():
    """
    邀请用户加入
    :param:
        group_id 发送者小组id
        user_email 用户邮箱
    """
    data = request.get_json()
    uid = jwt_util.get_id_from_jwt(request.headers.get('Authorization'))
    try:
        res = group.invite(data, uid)
    except BizException as e:
        return re.fail(e)
    return re.succeed(res)

@bp.route('/join', methods=['POST'])
def join():
    """
    用户加入小组
    :param:
        group_id 邀请码(小组id)
    """
    data = request.get_json()
    user_id = jwt_util.get_id_from_jwt(request.headers.get('Authorization'))
    try:
        res = group.join(data, user_id)
    except BizException as e:
        return re.fail(e)
    return re.succeed(res)

