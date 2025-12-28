import logging
import os

from qcloud_cos import CosConfig, CosS3Client
from qcloud_cos.cos_exception import CosException


class CosClient:
    Bucket = "exampaper-1384695153"
    sid = os.getenv("SECRET_ID")
    sk = os.getenv("SECRET_KEY")
    r = "ap-shanghai"

    def __init__(self):
        conf = CosConfig(Region=self.r, SecretId=self.sid, SecretKey=self.sk)
        try:
            self.client = CosS3Client(conf)
        except Exception as e:
            logging.error(f"COS客户端连接失败：{e}")
        else:
            logging.info("Cos客户端连接成功")

    def upload_from_fp(self, fp, key):
        """
        :param fp: 文件流
        :param key: 文件键 应确保前缀与小组目录一致
        :return: 是否成功
        """
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
        url = cos_client.client.get_presigned_url(
            Method="GET",
            Bucket=self.Bucket,
            Key=key,
            Expired=300,
        )
        return url

    def create_dir(self, _path: str):
        """
        创建目录 创建小组时应调用

        """
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
    path = f"{os.getcwd()}/demo.txt"
    with open(path) as f:
        cos_client.upload_from_fp(f, path)
