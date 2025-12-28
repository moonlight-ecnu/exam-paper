from backend.infra.entity.response import Response
from backend.infra.entity.group import Group

class GroupInfo(Response):
    def __init__(self, group:Group, member_names: dict = None):
        self.group_id = str(group.id)
        self.group_name = group.name
        self.group_members = group.members
        self.member_names = member_names if member_names else {}
        self.group_members_count = len(group.members)
        self.leader_id = str(group.leader)

    def to_dict(self):
        # Construct a list of members with role and name
        members_list = []
        for uid, is_admin in self.group_members.items():
            members_list.append({
                'user_id': uid,
                'user_name': self.member_names.get(uid, 'Unknown'),
                'role': 'admin' if str(uid) == self.leader_id else 'member'
            })

        return {
            'group_id': self.group_id,
            'group_name': self.group_name,
            'members': members_list, # New detailed list
            'group_members_count': self.group_members_count,
            'leader_id': self.leader_id
        }