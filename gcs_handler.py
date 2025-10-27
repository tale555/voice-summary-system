"""
Google Cloud Storage ハンドラーモジュール
長時間音声対応のためのGCS連携
"""

import os
import logging
from typing import Optional
from google.cloud import storage
from config import GOOGLE_APPLICATION_CREDENTIALS, GCS_BUCKET_NAME

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GCSHandler:
    """Google Cloud Storage ハンドラークラス"""

    def __init__(self, bucket_name: str = GCS_BUCKET_NAME):
        """
        初期化

        Args:
            bucket_name: GCSバケット名
        """
        self.bucket_name = bucket_name
        self.client = None
        self.bucket = None
        self._initialize_client()

    def _initialize_client(self):
        """Google Cloud Storage クライアントを初期化"""
        try:
            # 認証情報を設定
            if GOOGLE_APPLICATION_CREDENTIALS:
                if os.path.exists(GOOGLE_APPLICATION_CREDENTIALS):
                    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_APPLICATION_CREDENTIALS
                    logger.info(f"GCS認証情報を設定: {GOOGLE_APPLICATION_CREDENTIALS}")

            self.client = storage.Client()
            self.bucket = self.client.bucket(self.bucket_name)
            logger.info(f"Google Cloud Storage クライアントを初期化しました (バケット: {self.bucket_name})")

        except Exception as e:
            logger.error(f"GCSクライアント初期化エラー: {e}")
            raise

    def upload_file(self, local_file_path: str, gcs_file_name: Optional[str] = None) -> str:
        """
        ファイルをGCSにアップロード

        Args:
            local_file_path: ローカルファイルのパス
            gcs_file_name: GCS上のファイル名（省略時は自動生成）

        Returns:
            GCS URI (gs://bucket-name/file-name)
        """
        try:
            # GCSファイル名を生成（省略時は元のファイル名を使用）
            if gcs_file_name is None:
                gcs_file_name = os.path.basename(local_file_path)

            # アップロード
            blob = self.bucket.blob(gcs_file_name)
            blob.upload_from_filename(local_file_path)
            
            gcs_uri = f"gs://{self.bucket_name}/{gcs_file_name}"
            logger.info(f"ファイルをGCSにアップロードしました: {gcs_uri}")

            return gcs_uri

        except Exception as e:
            logger.error(f"GCSアップロードエラー: {e}")
            raise

    def delete_file(self, gcs_file_name: str):
        """
        GCSからファイルを削除

        Args:
            gcs_file_name: GCS上のファイル名
        """
        try:
            blob = self.bucket.blob(gcs_file_name)
            blob.delete()
            logger.info(f"GCSファイルを削除しました: {gcs_file_name}")

        except Exception as e:
            logger.warning(f"GCSファイル削除エラー: {e}")

    def file_exists(self, gcs_file_name: str) -> bool:
        """
        ファイルがGCSに存在するか確認

        Args:
            gcs_file_name: GCS上のファイル名

        Returns:
            存在する場合True
        """
        try:
            blob = self.bucket.blob(gcs_file_name)
            return blob.exists()
        except Exception as e:
            logger.error(f"GCSファイル存在確認エラー: {e}")
            return False


def create_gcs_handler(bucket_name: str = None) -> GCSHandler:
    """
    GCSハンドラーオブジェクトを作成

    Args:
        bucket_name: GCSバケット名

    Returns:
        GCSHandlerインスタンス
    """
    if bucket_name:
        return GCSHandler(bucket_name)
    else:
        return GCSHandler()
