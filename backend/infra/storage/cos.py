import logging
import os
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

sid = os.getenv("SECRET_ID")
sk = os.getenv("SECRET_KEY")
bn = os.getenv("BUCKET_NAME")
r = "ap-shanghai"

class CosClient:
    Bucket = bn


    def __init__(self):
        conf = CosConfig(Region=r, SecretId=sid, SecretKey=sk)
        try:
            self.client = CosS3Client(conf)
        except Exception as e:
            logging.error(f"COS客户端连接失败：{e}")
        else:
            logging.info("Cos客户端连接成功")

    def admin_upload(self, dir, file_key):
        """
        server端上传本地文件
        :param:
        dir 目标路径
        file_key 文件名
        """
        pass

    def user_download(self):
        """client端下载文件"""

    def create_dir(self, path:str):
        """创建目录"""
        try:
            self.client.put_object(
                Bucket=self.Bucket,
                Key=path,
                Body=b"",
            )
        except Exception as e:
            logging.error(f"目录{path}创建失败：{e}")


cos_client = CosClient() # 可导出供其他模块使用