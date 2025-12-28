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


@bp.route('/upload', methods=['POST'])
def upload():
    """
    用户向小组空间上传文件
    :param:
        file 文件
        group_id 小组id
        subject 学科
        year 年份
        paper_type 试卷类型(contest/exam/exercise)
            exam_type 考卷类型(monthly,mid,final)
        description 描述

    :return:
        file_info 文件信息类，包含access_url
    """
    data = request.get_json()
    uid = jwt_util.get_id_from_jwt(request.headers.get('Authorization'))
    file = request.files.get('file')
    try:
        res = group.upload(file, data, uid)
    except BizException as e:
        return re.fail(e)
    return re.succeed(res)


@bp.route('/download', methods=['POST'])
def download():
    """
    :param:
        group_id 小组id
        file_id 文件uid
        target_type 请求原始文件/生成文件
    :return:
        file_info/gen_file_info (生成)文件的信息，包含预签名url
    """
    data = request.get_json()
    uid = jwt_util.get_id_from_jwt(request.headers.get('Authorization'))
    try:
        res = group.download(data, uid)
    except BizException as e:
        return re.fail(e)
    return re.succeed(res)
