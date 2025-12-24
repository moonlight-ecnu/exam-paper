from backend.infra.entity.response import Response
from backend.infra.entity.group import Group

class GroupInfo(Response):
    def __init__(self, group:Group):
        self.group_id = str(group.id)
        self.group_name = group.name
        self.group_members = group.members
        self.group_members_count = len(group.members)

    def to_dict(self):
        return {
            'group_id': self.group_id,
            'group_name': self.group_name,
            'group_members': self.group_members,
            'group_members_count': self.group_members_count
        }