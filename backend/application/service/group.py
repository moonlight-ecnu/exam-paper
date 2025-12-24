import logging
from datetime import datetime

from mongoengine.errors import DoesNotExist

from backend.infra.entity.group import Group
from backend.infra.entity.user import User

from backend.application.dto.group_info import GroupInfo
from backend.infra.exception.errorcode import ErrorCode
from backend.infra.exception.exception import BizException as BE
from backend.infra.util import redis_util
# from backend.infra.storage.cos import cos_client
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
    if str(g.leader) != user_id: # 只有组长才能发出邀请
        raise BE.error(ErrorCode.INTERNAL_ERROR)

    # 缓存邀请
    cachekey = f"invite:{gid}-to-{target_email}"
    redis_util.set_kv_with_expire(cachekey,"")

    #TODO 发送邀请邮件，需包含group_id字符串作为 “邀请码”



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
def upload():
    """
    upload 上传文件到小组空间
    先上传到server(本机)，由server上传到Bucket
    """
    pass

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
