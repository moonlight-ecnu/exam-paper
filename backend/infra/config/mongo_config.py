import logging

from mongoengine import connect
from backend.infra.consts.database import MONGO_PORT, MONGO_HOST, MONGO_DB


def mongo_init():
    """初始化数据库连接"""
    try:
        connect(
            db=MONGO_DB,
            host=MONGO_HOST,
            port=MONGO_PORT,
        )
    except Exception as e:
        logging.error(f"MongoDB连接失败:{e}")
    else:
        logging.info("MongoDB连接成功")
