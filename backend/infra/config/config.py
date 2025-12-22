from backend.infra.config.redis_config import redis_init
from backend.infra.config.mongo_config import mongo_init
from backend.infra.config.log_config import log_init

def init_app(app):
    """加载环境变量，初始化所有配置"""
    mongo_init()
    log_init()
    redis_init(app)
