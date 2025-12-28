import logging
import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from backend.infra.consts.smtp import SENDER, SUBJECT, SMTP_PORT, SMTP_SERVER, AUTHORIZATION_CODE, VERIFY_CODE_TEMPLATE

from backend.infra.util import redis_util


def send_verify_code(target: str) -> str:
    """向{target}发送验证码，并存储 [邮箱-验证码]"""
    # 创建邮件
    message = MIMEMultipart()
    message['From'] = SENDER
    message['To'] = target
    message['Subject'] = SUBJECT
    # 生成并存储验证码
    code = set_verify_code(target)
    # 邮件正文
    html_content = VERIFY_CODE_TEMPLATE.replace("{verification_code}", code)
    html_part = MIMEText(html_content, 'html', 'utf-8')
    message.attach(html_part)

    # 连接到qq smtp服务器并发送
    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)  # 链接SMTP服务器
        server.login(SENDER, AUTHORIZATION_CODE)  # 登录SMTP服务器

        server.sendmail(SENDER, target, message.as_string())
        server.quit()
        return code
    except Exception as e:
        logging.error(e)
        return ""


def set_verify_code(target: str):
    """
    生成6位数字验证码并存储至redis中，返回生成的验证码
    """
    code = ''.join(random.choices(string.digits, k=6))
    logging.info(f"verify code of {target} is {code}")
    redis_util.set_kv_with_expire(f"verify:{target}", code)  # 默认5分钟过期
    return code


def check_verify_code(target: str, verify_code: str):
    code = redis_util.get_value(f"verify:{target}")
    if code is None:
        return False
    return verify_code == code.decode('utf-8')
