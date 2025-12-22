import logging

import redis

from backend.infra.consts.database import REDIS_HOST, REDIS_PORT, REDIS_DB


def redis_init(the_app):
    """初始化redis连接"""
    try:
        pool = redis.ConnectionPool(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
        )
        redis_client = redis.Redis(connection_pool=pool)
        logging.info("Redis连接成功")
        the_app.extensions["redis_client"] = redis_client
    except Exception as e:
        logging.error(f"Redis连接失败: {e}")
