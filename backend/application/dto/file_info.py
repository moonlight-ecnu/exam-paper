from backend.infra.entity.file import File
from backend.infra.entity.response import Response


class FileInfo(Response):
    """
    FileInfo 返回给前端的文件信息类
    """

    def __init__(self, file: File):
        # 基础信息（必须返回）
        self.file_id = file.id
        self.filename = file.filename
        self.url = file.url  # 访问URL（暂使用本地存储path）
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
        """转换为字典，注意处理None值"""
        result = {
            "file_id": str(self.file_id) if self.file_id else None,
            "filename": self.filename,
            "url": self.url,
            "author": self.author,
            "group_id": self.group_id,
            "created_at": self.created_at,
            "subject": self.subject,
            "year": self.year,
            "description": self.description,
            "content_type": self.content_type,
        }

        # 只有在content_type为exam时才返回exam_type
        if self.content_type == "exam" and self.exam_type:
            result["exam_type"] = self.exam_type

        # 保留可能的None值
        return result