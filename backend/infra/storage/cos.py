import logging
import os

from qcloud_cos import CosConfig, CosS3Client
from qcloud_cos.cos_exception import CosException
from backend.infra.config.config import conf

class CosClient:
    def __init__(self):
        self.client = None
        self.Bucket = None

    def _ensure_client(self):
        if self.client:
            return

        # Prefer loading from conf, fallback to env or defaults
        self.Bucket = conf.get("BUCKET_NAME", os.getenv("BUCKET_NAME", "exampaper-1384695153"))
        self.sid = conf.get("SECRET_ID", os.getenv("SECRET_ID"))
        self.sk = conf.get("SECRET_KEY", os.getenv("SECRET_KEY"))
        self.r = conf.get("REGION", os.getenv("REGION", "ap-shanghai"))

        if not self.sid or not self.sk:
            logging.warning("COS SecretID or SecretKey not found in config.")
            return

        conf_cos = CosConfig(Region=self.r, SecretId=self.sid, SecretKey=self.sk)
        try:
            self.client = CosS3Client(conf_cos)
            logging.info("Cos客户端连接成功")
        except Exception as e:
            logging.error(f"COS客户端连接失败：{e}")
            self.client = None

    def upload_from_fp(self, fp, key):
        """
        :param fp: 文件流
        :param key: 文件键 应确保前缀与小组目录一致
        :return: 是否成功
        """
        self._ensure_client()
        if not self.client:
            raise Exception("COS client not initialized")
        try:
            self.client.put_object(
                Bucket=self.Bucket,
                Key=key,
                Body=fp,
            )
        except CosException as e:
            logging.error(e)
            raise e
        else:
            return True

    def from_path(self, _path, key):
        """
        :param _path: 本地文件路径
        :param key: 文件键 应确保前缀与小组目录一致
        :return: 是否成功
        """
        self._ensure_client()
        if not self.client:
            raise Exception("COS client not initialized")
        # 根据文件大小自动选择分块大小,多线程并发上传提高上传速度
        try:
            self.client.upload_file(
                Bucket=self.Bucket,
                Key=key,
                LocalFilePath=_path
            )
        except CosException as e:
            logging.error(e)
            raise e
        else:
            return True

    def gen_signed_url(self, key) -> str:
        """
        生成预签名url 供client端下载文件
        """
        self._ensure_client()
        if not self.client:
            return ""
        try:
            url = self.client.get_presigned_url(
                Method="GET",
                Bucket=self.Bucket,
                Key=key,
                Expired=300,
            )
            return url
        except Exception as e:
            logging.error(f"Generate signed url failed: {e}")
            return ""

    def create_dir(self, _path: str):
        """
        创建目录 创建小组时应调用
        """
        self._ensure_client()
        if not self.client:
            return
        try:
            self.client.put_object(
                Bucket=self.Bucket,
                Key=_path,
                Body=b"",
            )
        except CosException as e:
            logging.error(f"小组目录[{_path}]创建失败：{e}")


cos_client = CosClient()  # 单例模式 可导出供其他模块使用

if __name__ == "__main__":
    # Test
    pass
