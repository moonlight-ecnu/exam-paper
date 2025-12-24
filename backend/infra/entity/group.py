from datetime import datetime

from mongoengine import Document, StringField, DateTimeField, DictField, IntField
from backend.infra.consts.entity import MAX_MEMBER_NUM


class Group(Document):
    name = StringField(required=True)
    members = DictField(required=True)  # 用一个字典维护所有成员：用户id-组内权限{user_id：isAdmin} 限制人数上限
    leader = StringField(required=True)  # 创建者
    member_num = IntField(default=MAX_MEMBER_NUM)  # 小组人数上限，默认为7
    created_at = DateTimeField(default=datetime.now)

    def has_member(self, user_id):
        """返回小组是否有指定成员"""
        return user_id in self.members

    def get_member_role(self, user_id):
        """返回组内成员权限-是否是admin"""
        return self.members.get(user_id)

    def count_member(self):
        return self.members.count()

class Invitation(Document):
    """小组相关的邀请"""
    target = StringField(required=True) # 被邀请人(邮箱?)
    leader = StringField(required=True) # 发起人(邮箱?)
    group = StringField(required=True) # 小组id
    created_at = DateTimeField(default=datetime.now)
    status = IntField(default=0) # 状态 采用枚举值 0-待处理；1-已接受；2-已拒绝