"""
Google Cloud Speech-to-Text API の設定ファイル
"""

# サポートする音声ファイル形式
SUPPORTED_AUDIO_FORMATS = [
    'wav', 'mp3', 'flac', 'ogg', 'm4a', 'webm'
]

# 音声認識の設定
SPEECH_CONFIG = {
    'encoding': 'LINEAR16',  # より一般的なエンコーディング
    # 'sample_rate_hertz': 16000,  # サンプルレートはファイルから自動判定
    'language_code': 'ja-JP',  # 日本語
    'enable_automatic_punctuation': True,  # 自動句読点
    'enable_word_time_offsets': False,  # 無効化して高速化
    'model': 'default',  # デフォルトモデル
}

# 音声ファイルの最大サイズ（MB）
MAX_AUDIO_SIZE_MB = 100

# 音声ファイルの最大長（秒）
MAX_AUDIO_DURATION_SECONDS = 3600  # 1時間
