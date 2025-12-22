from backend.infra.entity.response import Response

class BizException(Exception, Response):
    def __init__(self, code, msg):
        super().__init__(msg)
        self.code = code
        self.msg = msg

    @classmethod
    def error(cls, error_code):
        return cls(error_code.code, error_code.msg)

    def to_dict(self):
        return {
            'code': self.code,
            'msg': self.msg,
        }
