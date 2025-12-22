from backend.infra.entity.response import Response
from backend.infra.entity.user import User
from backend.infra.util.jwt_util import create_jwt


class UserInfo(Response):
    """
    UserInfo 返回给前端的用户信息类
    """
    def __init__(self, user: User):
        self.user_id = user.id
        self.name = user.name
        self.email = user.email
        self.token = create_jwt({"id": str(user.id)}) # 将用户_id放入jwt中

    def to_dict(self)->dict:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "token": self.token
        }


