from datetime import datetime

from mongoengine import Document, StringField, LongField, DateTimeField

class User(Document):
    email = StringField(required=True)  # 邮箱
    user_name = StringField(required=True)
    avatar = StringField(required=True)  # 图片url
    pwd = StringField(required=True)  # 需要加密存储

    created_at = DateTimeField(default=datetime.now)