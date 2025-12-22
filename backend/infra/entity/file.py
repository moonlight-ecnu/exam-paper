from datetime import datetime

from mongoengine import Document, EmbeddedDocument, StringField, DateTimeField, EmbeddedDocumentField, DictField

class MetaInfo(EmbeddedDocument):
    """文件的基本信息"""

    subject = StringField(required=True)  # 学科：english/operating_system等
    year = StringField()  # 年份
    description = StringField(default=None)  # 描述
    content_type = StringField(required=True)  # contest/exam/exercise
    exam_type = StringField(default=None)  # monthly/mid/final (仅当content_type=exam时有效)


class File(Document):
    author_id = StringField(required=True)  # 上传者用户id
    group_id = StringField(required=True)  # 上传到的组id
    filename = StringField(required=True)  # 文件名
    url = StringField(required=True)  # 访问url（暂使用本地存储path）
    meta_info = EmbeddedDocumentField(MetaInfo, required=True)
    created_at = DateTimeField(default=datetime.now)

class ProcessedContent(Document):
    """
    原始文件经大模型处理后的输出文件，暂定html类型 创建时会利用多模态大模型的api以理解图表
    要求：
        1.格式美观（prompt给完纯靠模型发挥）
        2.每道题提供“问ai”按钮，调用非多模态模型的api，把整道题(题干、选项、文本化表示的图表)作为输入 TODO需要实现相关接口
        3.总结/预览信息
    """
    url = StringField(required=True)  # 处理后的内容访问URL（暂使用本地存储path）
    title = StringField(required=True) # 标题
    source_id = StringField(required=True)  # 原始文件ID
    group_id = StringField(required=True)  # 所属小组ID
    preview_data = DictField(default={})  # 预览信息：题数、预估时间等
    status = StringField(default='active')  # active/deleted
    created_at = DateTimeField(default=datetime.now)