class Response:
    """返回给前端的响应基类 所有返回给前端的类需要继承该类并重写to_dict方法"""
    def to_dict(self):
        raise NotImplementedError