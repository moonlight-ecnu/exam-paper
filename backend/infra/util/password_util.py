import hashlib


def md5_encrypt(password):
    """使用md5加密明文密码，返回密文结果"""
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    encrypted_password = md5.hexdigest()
    return encrypted_password