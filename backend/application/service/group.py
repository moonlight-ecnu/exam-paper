import logging
from datetime import datetime
from fileinput import filename

from mongoengine.errors import DoesNotExist

from backend.infra.consts.storage import GROUP_COS_PATH_ORIGIN, GROUP_COS_PATH_GEN
from backend.infra.storage.cos import cos_client

from backend.application.dto.file_info import FileInfo, GenFileInfo
from backend.application.dto.group_info import GroupInfo

from backend.infra.entity.file import MetaInfo, File, GenFile
from backend.infra.entity.group import Group
from backend.infra.entity.user import User

from backend.infra.exception.errorcode import ErrorCode
from backend.infra.exception.exception import BizException as BE

from backend.infra.util import redis_util
from backend.infra.util.req_util import get_param


# 小组管理相关
def create(data, user_id):
    """创建小组"""
    name = get_param("name", data)
    try:
        g = Group(
            name=name,
            members={user_id: True},
            leader=user_id,
            created_at=datetime.now(),
        )
        g.save()
    except Exception as e:
        logging.error(e)
        raise BE.error(ErrorCode.REGISTER_FAILED)
    # 创建小组目录
    cos_client.create_dir(GROUP_COS_PATH.format(group_id=str(g.id)))
    return GroupInfo(g)


def dismiss(data):
    """解散小组"""
    pass


def invite(data, user_id):
    """
    邀请用户加入小组
    基于redis，创建邀请缓存
    """
    gid = get_param("group_id", data)
    target_email = get_param("user_email", data)
    # 参数校验 组存在性
    try:
        g = Group.objects.get(id=gid)
    except DoesNotExist:
        raise BE.error(ErrorCode.GROUP_NOT_FOUND)
    if str(g.leader) != user_id:  # 只有组长才能发出邀请
        raise BE.error(ErrorCode.INTERNAL_ERROR)

    # 缓存邀请
    cachekey = f"invite:{gid}-to-{target_email}"
    redis_util.set_kv_with_expire(cachekey, "")

    # TODO 发送邀请邮件，需包含group_id字符串作为 “邀请码”


def join(data, user_id):
    """
    受邀请加入小组
    :param:
        group_id 小组id
    """
    gid = get_param("group_id", data)
    # 查询用户邮箱
    try:
        user = User.objects.get(id=user_id)
    except DoesNotExist:
        raise BE.error(ErrorCode.USER_NOT_FOUND)

    # 检查邀请缓存
    cachekey = f"invite:{gid}-to-{user.email}"
    if not redis_util.has_key(cachekey):
        raise BE.error(ErrorCode.GROUP_NOT_INVITED)  # 未被邀请

    # 检查小组存在
    try:
        g = Group.objects.get(id=gid)
    except DoesNotExist:
        raise BE.error(ErrorCode.GROUP_NOT_FOUND)
    # 加入成员
    g.members[user_id] = False
    g.save()
    # 删除邀请缓存
    redis_util.delete_kv(cachekey)

    return GroupInfo(g)


# 小组空间使用相关 文件上传、管理
def upload(file, data, user_id):
    """
    upload 上传文件到小组空间
    先上传到server(本机)，由server上传到Bucket
    """
    # 参数提取
    if file is None:
        raise BE.error(ErrorCode.INVALID_PARAMETER)
    group_id = get_param("group_id", data)
    subject = get_param("subject", data)
    year = get_param("year", data)
    paper_type = get_param("paper_type", data) # 试卷类型：考试/竞赛
    exam_type = data.get("exam_type")
    description = data.get("description", "")

    # 小组相关校验
    try:
        g = Group.objects.get(id=group_id) # 小组存在
    except DoesNotExist:
        raise BE.error(ErrorCode.GROUP_NOT_FOUND)

    if not g.has_member(user_id): # 小组有成员
        raise BE.error(ErrorCode.GROUP_NO_MEMBER)

    # 构建对象键："{组prefix}/origin/{时间戳字符串}/{文件名}" 用于存入db、调用cos进行上传
    ts = datetime.now().strftime("%Y%m%d%H%M%S") # 时间戳
    fn = file.filename
    ock = f"{GROUP_COS_PATH_ORIGIN}{ts}/{fn}"

    # 构建原始文件的[数据库document]并存储
    db_file = File(
        author_id=user_id,
        group_id=group_id,
        filename=fn, # 从网络传输的file中得到文件名
        cos_key=ock,
        meta_info=MetaInfo(
            subject=subject,
            year=year,
            description=description,
            content_type=paper_type,
            exam_type=exam_type,
        )
    )
    db_file.save()

    # 上传原文件至cos

    # 调用模型并创建生成文件

    # 对象键
    gck = ""
    # 构建生成文件的[数据库document]并存储
    gen_file = GenFile()
    gen_file.save()

    # 上传生成文件至cos

    # 返回空响应，controller层使用re.success返回


def delete_file():
    """
    逻辑删除文件
    :return:
    """
    pass


def list_files():
    """
    列出小组内符合filter的所有文件
    - 要求前端给出规范且有效的filter
    - mvp版本中暂时不提供filter功能
    """
    pass


def download(data, user_id):
    """
    获取单个（生成）文件
    :param:
        group_id 小组id
        file_id 文件uid
        target_type 请求原始文件/生成文件
    :return:
        file_info/gen_file_info (生成)文件的信息，包含预签名url
    """
    group_id = get_param("group_id", data)
    file_id = get_param("file_id", data)
    target_type = get_param("target_type", data)  # "origin" or "gen"

    # 小组校验
    try:
        g = Group.objects.get(id=group_id)
    except DoesNotExist:
        raise BE.error(ErrorCode.GROUP_NOT_FOUND)
    if not g.has_member(user_id):
        raise BE.error(ErrorCode.GROUP_NO_MEMBER)

    # 检索数据库得到文件
    if target_type == "origin":
        try:
            db_f = File.objects.get(id=file_id, group_id=group_id)
        except DoesNotExist:
            raise BE.error(ErrorCode.DB_NOT_FOUND)
        return FileInfo(db_f)
    
    elif target_type == "gen":
        try:
            db_f = GenFile.objects.get(id=file_id, group_id=group_id)
        except DoesNotExist:
            raise BE.error(ErrorCode.DB_NOT_FOUND)
        return GenFileInfo(db_f)
    
    else:
        raise BE.error(ErrorCode.INVALID_REQUEST_TYPE)


