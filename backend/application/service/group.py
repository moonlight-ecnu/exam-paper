import logging
from datetime import datetime

from mongoengine.errors import DoesNotExist

from backend.infra.consts.storage import GROUP_COS_PATH, GROUP_COS_PATH_ORIGIN, GROUP_COS_PATH_GEN
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
from backend.infra.util.completion import parser_img_bytes


def _get_group_info_with_members(g):
    """Helper to create GroupInfo with member names"""
    try:
        member_ids = list(g.members.keys())
        users = User.objects(id__in=member_ids)
        member_names = {str(u.id): u.user_name for u in users}
        return GroupInfo(g, member_names)
    except Exception as e:
        logging.error(f"Error fetching group members: {e}")
        return GroupInfo(g)

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
    return _get_group_info_with_members(g)


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
    # Optional fields
    year = data.get("year")
    paper_type = get_param("paper_type", data) # 试卷类型：考试/竞赛
    exam_type = data.get("exam_type")
    description = data.get("description", "")

    # 小组相关校验
    try:
        g = Group.objects.get(id=group_id) # 小组存在
    except DoesNotExist:
        raise BE.error(ErrorCode.GROUP_NOT_FOUND)
    except ValidationError:
        raise BE.error(ErrorCode.INVALID_PARAMETER)

    if not g.has_member(user_id): # 小组有成员
        raise BE.error(ErrorCode.GROUP_NO_MEMBER)

    # Read file content
    file_content = file.read()
    if not file_content:
        raise BE.error(ErrorCode.INVALID_PARAMETER)

    # 构建对象键："{组prefix}/origin/{时间戳字符串}/{文件名}" 用于存入db、调用cos进行上传
    ts = datetime.now().strftime("%Y%m%d%H%M%S") # 时间戳
    fn = file.filename
    ock = f"{GROUP_COS_PATH_ORIGIN.format(group_id=group_id)}{ts}/{fn}"

    # 1. 上传原文件至cos
    try:
        cos_client.upload_from_fp(file_content, ock)
    except Exception as e:
        logging.error(f"COS Upload Origin Failed: {e}")
        raise BE.error(ErrorCode.INTERNAL_ERROR)

    # 2. 构建原始文件的[数据库document]并存储
    try:
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
    except Exception as e:
        logging.error(f"DB Save File Failed: {e}")
        raise BE.error(ErrorCode.INTERNAL_ERROR)

    # 3. 调用模型并创建生成文件
    try:
        html_content = parser_img_bytes(file_content)
    except Exception as e:
        logging.error(f"Model Generation Failed: {e}")
        # Return success for origin file, but log error for generation
        return FileInfo(db_file)

    # 4. 上传生成文件至cos
    gck = f"{GROUP_COS_PATH_GEN.format(group_id=group_id)}{ts}/{fn}.html"
    try:
        cos_client.upload_from_fp(html_content.encode('utf-8'), gck)
    except Exception as e:
        logging.error(f"COS Upload Gen Failed: {e}")
        return FileInfo(db_file)

    # 5. 构建生成文件的[数据库document]并存储
    try:
        gen_file = GenFile(
            cos_key=gck,
            title=f"Parsed: {fn}",
            source_id=str(db_file.id),
            group_id=group_id,
            preview_data={}, 
            status='active'
        )
        gen_file.save()
    except Exception as e:
        logging.error(f"DB Save GenFile Failed: {e}")

    return FileInfo(db_file)


def delete_file():
    """
    逻辑删除文件
    :return:
    """
    pass


def list_files(data, user_id):
    """
    列出小组内符合filter的所有文件
    """
    group_id = get_param("group_id", data)

    # Check group permission
    try:
        g = Group.objects.get(id=group_id)
    except DoesNotExist:
        raise BE.error(ErrorCode.GROUP_NOT_FOUND)
    if not g.has_member(user_id):
        raise BE.error(ErrorCode.GROUP_NO_MEMBER)

    # Filter files
    files = File.objects(group_id=group_id).order_by('-created_at')
    
    # Return file list
    return [FileInfo(f).to_dict() for f in files]

def my_groups(user_id):
    """
    列出用户加入的所有小组
    """
    # Using raw query or iterating. MongoEngine doesn't support querying keys of DictField easily in older versions
    # But we can query where "members.user_id" exists.
    # However, members is DictField. 
    # Alternative: iterate all groups (inefficient) or better schema.
    # For MVP, let's use a simple scan or assume schema supports query.
    # Actually, we can use __raw__ query for mongodb
    
    # Using Q object for more complex queries if needed, but for DictField key existence:
    # groups = Group.objects(members__haskey=user_id) # This syntax might vary
    
    # Let's fallback to raw query which is reliable
    groups = Group.objects(__raw__={f"members.{user_id}": {"$exists": True}})
    
    return [_get_group_info_with_members(g).to_dict() for g in groups]

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
            # First try to find by ID directly (if frontend passed gen file ID)
            db_f = GenFile.objects.get(id=file_id, group_id=group_id)
        except (DoesNotExist, Exception):
             # Fallback: try to find by source_id (if frontend passed origin file ID)
            try:
                db_f = GenFile.objects.get(source_id=file_id, group_id=group_id)
            except DoesNotExist:
                raise BE.error(ErrorCode.DB_NOT_FOUND)
        return GenFileInfo(db_f)
    
    else:
        raise BE.error(ErrorCode.INVALID_REQUEST_TYPE)
