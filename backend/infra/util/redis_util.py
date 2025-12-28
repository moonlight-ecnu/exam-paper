import logging

from flask import current_app
from redis import RedisError


def set_kv(key, value):
    r = current_app.extensions["redis_client"]
    try:
        logging.info(f"redis set {key}:{value}")
        r.set(key, value)
    except RedisError as e:
        logging.error(f"redis set failed with error {e}")
        return False
    return True


def set_kv_with_expire(key, value, expire=3000):
    r = current_app.extensions["redis_client"]
    try:
        logging.info(f"redis set {key}:value with expire {expire}s")
        r.set(key, value, ex=expire)
    except RedisError as e:
        logging.error(f"redis set failed with error {e}")
        return False
    return True


def get_value(key):
    r = current_app.extensions["redis_client"]
    try:
        return r.get(key)
    except RedisError as e:
        logging.error(f"redis get key:[ {key} ] failed with error {e}")


def has_key(key):
    r = current_app.extensions["redis_client"]
    try:
        return r.exists(key)
    except RedisError as e:
        logging.error(f"redis get key:[ {key} ] failed with error {e}")


def delete_kv(key):
    r = current_app.extensions["redis_client"]
    try:
        r.delete(key)
    except RedisError as e:
        pass  # 删除失败不影响，过期也会自动处理
