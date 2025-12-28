import os
import yaml
import logging

# Global config object
conf = {}

def load_config():
    global conf
    # Determine the project root. Assuming this file is in backend/infra/config/
    # So we go up 3 levels to reach backend/ and then up 1 more to reach project root.
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    config_path = os.path.join(base_dir, 'etc', 'config.yaml')
    
    if not os.path.exists(config_path):
        # Fallback for development if run from different dir or just try relative
        if os.path.exists('etc/config.yaml'):
             config_path = 'etc/config.yaml'

    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            try:
                conf.update(yaml.safe_load(f))
                # logging.info(f"Loaded config from {config_path}") # Log might not be init yet
            except yaml.YAMLError as exc:
                print(f"Error loading config: {exc}")
    else:
        print(f"Config file not found at {config_path}")

    # Set environment variables for compatibility
    for k, v in conf.items():
        if isinstance(v, (str, int, float)):
            os.environ[str(k)] = str(v)

from backend.infra.config.redis_config import redis_init
from backend.infra.config.mongo_config import mongo_init
from backend.infra.config.log_config import log_init

def init_app(app):
    """加载环境变量，初始化所有配置"""
    load_config()
    log_init() # Init log after config load (though log_init might not depend on it yet)
    logging.info("Configuration loaded.")
    mongo_init()
    redis_init(app)
