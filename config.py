"""
音声要約システムの設定ファイル
"""

import os
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# Google Cloud Speech-to-Text API 設定
# Railway対応: 環境変数からJSONを読み込む場合の処理
_script_dir = os.path.dirname(os.path.abspath(__file__))
_default_credentials = os.path.join(_script_dir, 'configs', 'service-account-key.json')

# 環境変数からJSONファイルの内容を取得（Railway用）
_credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
if _credentials_json:
    # 環境変数からJSONが設定されている場合、一時ファイルを作成
    import json
    import tempfile
    _temp_credentials = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    json.dump(json.loads(_credentials_json), _temp_credentials)
    _temp_credentials.close()
    GOOGLE_APPLICATION_CREDENTIALS = _temp_credentials.name
else:
    # 通常のファイルパスで読み込む
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', _default_credentials)

# OpenAI API 設定
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

# Flask 設定
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

# アップロード設定
UPLOAD_FOLDER = os.path.join(_script_dir, 'uploads')
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB

# 出力設定
OUTPUT_FOLDER = os.path.join(_script_dir, 'outputs')

# Google Cloud Storage 設定
GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME', 'voice-summary-audio')
