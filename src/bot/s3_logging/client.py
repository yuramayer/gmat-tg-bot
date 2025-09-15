"""S3 Client wrapper for the cloud logging"""

import json
import boto3
from botocore.config import Config
from src.local_logger import LocalLogger


class S3Client:
    """The wrapper around boto3 S3 client"""

    def __init__(
            self,
            access_key: str,
            secret_key: str,
            bucket_name: str,
            endpoint_url: str = "https://storage.yandexcloud.net",
            region_name: str = "ru-central1"
            ):
        """Initialize the S3 Client"""
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name
        self._s3 = boto3.client(
            service_name="s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=endpoint_url,
            region_name=region_name,
            config=Config(signature_version="s3v4")
        )
        self.logger = LocalLogger("s3client_logger")
        self.logger.info('The S3 client is initialized')

    @staticmethod
    def get_log_key(
            timestamp: str,
            user_id: int
            ) -> str:
        """Generate partitioned S3 key for the log"""
        date, time_str = timestamp.split('T')
        hour = time_str[:2]
        return f"date={date}/hour={hour}/{user_id}_{timestamp}.json"

    def send_logs(
            self,
            logs_json: dict,
            key: str
            ) -> None:
        """Upload log dict as JSON to S3"""
        self._s3.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=json.dumps(
                logs_json,
                ensure_ascii=False
            ).encode("utf-8")
        )
