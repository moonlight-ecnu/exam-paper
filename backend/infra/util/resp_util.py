from flask import jsonify,abort

from backend.infra.entity.response import Response
from backend.infra.exception.exception import BizException

"""
ResponseUtil 工具
将响应转换为json格式, 以便返回前端
如果payload为Response及其子类的实现, 调用to_dict()方法变成json字符串
"""

def succeed(payload, code=0, msg="success"):
    if isinstance(payload, Response):
        return jsonify({"code": code, "msg": msg, "payload": payload.to_dict()})
    else:
        return jsonify({"code": code, "msg": msg, "payload": payload})


def fail(payload, code=999, msg="unknown error"):
    if isinstance(payload, BizException):  # 若返回值为业务异常类, 则不应该有payload, 只返回code和msg
        if payload.code == 1000 or payload.code == 1001:
            abort(403)
        return jsonify({"code": payload.code, "msg": payload.msg})
    elif isinstance(payload, Response):  # 若返回值为响应类, 需要有payload
        return jsonify({"code": code, "msg": msg, "payload": payload.to_dict()})
    else:
        return jsonify({"code": code, "msg": msg, "payload": payload})