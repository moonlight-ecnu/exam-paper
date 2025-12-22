import logging

from flask import Flask

from backend.infra.config.config import init_app

from backend.infra.util.smtp_util import send_verify_code, check_verify_code


def create_app():
    app = Flask(__name__)

    # 注册blueprint


    # 初始化数据库连接和基础组件
    init_app(app)

    return app


app = create_app()

if __name__ == '__main__':
    logging.info("Application started")
    app.run("0.0.0.0", port=5000)

    # 测试邮件验证
    # with app.app_context():
    #     target = "3071466454@qq.com"
    #     res = send_verify_code(target)
    #     if res:
    #         logging.info("Verify code sent successfully")
    #
    #         verify_code = input("请输入收到的验证码: ")
    #         success = check_verify_code(target, verify_code)
    #
    #         if success:
    #             print("验证码正确，校验成功！")