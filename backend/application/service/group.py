from backend.infra.entity.group import Group
from backend.infra.entity.group import Invitation
from backend.infra.storage.cos import cos_client


# 小组管理相关
def create(data):
    """创建小组"""
    pass

def dismiss(data):
    """解散小组"""
    pass

def invite(data):
    """邀请用户加入小组"""
    pass

def accept_invite(data):
    pass

def reject_invite(data):
    pass

# 小组空间使用相关 文件上传、管理
def upload():
    """
    upload 上传文件到小组空间
    先上传到server(本机)，由server上传到Bucket
    """
    cos_client.admin_upload()
    pass

def delete_file():
    """
    逻辑删除文件
    :return:
    """
    pass

def list_files(): # TODO
    """
    列出小组内符合filter的所有文件
    - 要求前端给出规范且有效的filter
    """
    pass
