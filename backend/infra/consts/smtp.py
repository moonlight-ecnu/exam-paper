import os

SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465
SUBJECT = "[ExamPaper@test]"
SENDER = "3071466454@qq.com"
AUTHORIZATION_CODE = os.environ.get("SMTP_AUTH")

VERIFY_CODE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        .code {
            font-size: 32px;
            font-weight: bold;
            color: #e74c3c;
            letter-spacing: 8px;
            font-family: 'Consolas', monospace;
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            border-radius: 8px;
            margin: 20px 0;
            user-select: all;
            cursor: pointer;
            border: 2px solid #e1e1e1;
        }
        .hint {
            color: #666;
            font-size: 14px;
            text-align: center;
        }
    </style>
</head>
<body>
    <p>您正在登录/注册 ExamPaper</p>

    <div class="code">{verification_code}</div>

    <div class="hint">
        点击上方验证码可全选复制<br>
        有效时间：5分钟
    </div>

    <p style="color: #999; font-size: 12px; margin-top: 30px;">
        请勿将验证码泄露给他人。如非本人操作，请忽略此邮件。
    </p>
</body>
</html>
"""

INVITATION_TEMPLATE = """"""