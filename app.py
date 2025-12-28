import logging

from flask import Flask
from flask_cors import CORS

from backend.infra.config.config import init_app
from backend.adaptor.bp import register_bp
from backend.infra.util.smtp_util import send_verify_code, check_verify_code


def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    # 注册blueprint
    register_bp(app)

    # 初始化数据库连接和基础组件
    init_app(app)

    return app


app = create_app()

if __name__ == '__main__':
    logging.info("Application started")
    app.run("127.0.0.1", port=5000, debug=True)
