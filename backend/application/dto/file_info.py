from backend.infra.entity.file import File, GenFile
from backend.infra.entity.response import Response

from backend.infra.storage.cos import cos_client

class FileInfo(Response):
    """
    FileInfo 返回给前端的文件信息类
    """

    def __init__(self, file: File):
        # 基础信息
        self.file_id = file.id
        self.filename = file.filename
        self.url = cos_client.gen_signed_url(file.cos_key)
        self.author = file.author_id  # 上传者用户ID
        self.group_id = file.group_id  # 所属小组ID
        self.created_at = file.created_at.isoformat() if file.created_at else None

        # 元数据信息（用于筛选和展示）
        if file.meta_info:
            self.subject = file.meta_info.subject  # 学科 - 重要筛选字段
            self.year = file.meta_info.year  # 年份 - 重要筛选字段
            self.description = file.meta_info.description  # 描述
            self.content_type = file.meta_info.content_type  # contest/exam/exercise - 重要
            self.exam_type = file.meta_info.exam_type if file.meta_info.content_type == "exam" else None
        else:
            self.subject = None
            self.year = None
            self.description = None
            self.content_type = None
            self.exam_type = None

    def to_dict(self) -> dict:
        """转换为嵌套字典，meta_info为嵌套json"""
        meta_info = {
            "subject": self.subject,
            "year": self.year,
            "description": self.description,
            "content_type": self.content_type,
        }
        if self.content_type == "exam" and self.exam_type:
            meta_info["exam_type"] = self.exam_type

        result = {
            "file_id": str(self.file_id) if self.file_id else None,
            "filename": self.filename,
            "url": self.url,
            "author": self.author,
            "group_id": self.group_id,
            "created_at": self.created_at,
            "meta_info": meta_info,
        }
        return result

class GenFileInfo(Response):
    """
    GenFileInfo 返回给前端的生成文件信息类
    """

    def __init__(self, gen_file: GenFile):
        self.file_id = gen_file.id
        self.filename = gen_file.title
        self.url = cos_client.gen_signed_url(gen_file.cos_key)
        self.group_id = gen_file.group_id
        self.source_id = gen_file.source_id
        self.preview_data = gen_file.preview_data or {}
        self.status = gen_file.status
        self.created_at = gen_file.created_at.isoformat() if gen_file.created_at else None

    def to_dict(self) -> dict:
        result = {
            "file_id": str(self.file_id) if self.file_id else None,
            "filename": self.filename,
            "url": self.url,
            "group_id": self.group_id,
            "source_id": self.source_id,
            "preview_data": self.preview_data,
            "status": self.status,
            "created_at": self.created_at,
        }
        # 保留可能的None值
        return result