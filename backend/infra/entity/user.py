from datetime import datetime

from mongoengine import Document, StringField, LongField, DateTimeField

from backend.infra.consts.database import DEFAULT_AVATAR


class User(Document):
    email = StringField(required=True)  # 邮箱
    user_name = StringField(required=True)
    pwd = StringField(required=True)  # 需要加密存储

    created_at = DateTimeField(default=datetime.now)