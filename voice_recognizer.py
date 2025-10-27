"""
音声認識機能のメインモジュール
Google Cloud Speech-to-Text APIを使用して音声をテキストに変換
"""

import os
import io
import logging
import tempfile
from typing import Optional, Dict, Any
from google.cloud import speech
from google.cloud.speech import RecognitionConfig, RecognitionAudio
from configs.speech_config import SUPPORTED_AUDIO_FORMATS, SPEECH_CONFIG, MAX_AUDIO_SIZE_MB, MAX_AUDIO_DURATION_SECONDS
from convert_audio import convert_to_wav
from gcs_handler import GCSHandler

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceRecognizer:
    """音声認識クラス"""
    
    def __init__(self, credentials_path: Optional[str] = None):
        """
        初期化
        
        Args:
            credentials_path: Google Cloud認証情報のパス
        """
        self.client = None
        self.credentials_path = credentials_path
        self._initialize_client()
    
    def _initialize_client(self):
        """Google Cloud Speech クライアントを初期化"""
        try:
            logger.info(f"認証情報パスの確認: {self.credentials_path}")
            
            if self.credentials_path:
                if os.path.exists(self.credentials_path):
                    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.credentials_path
                    logger.info(f"認証情報を設定: {self.credentials_path}")
                else:
                    logger.error(f"認証情報ファイルが見つかりません: {self.credentials_path}")
                    raise FileNotFoundError(f"File {self.credentials_path} was not found.")
            
            self.client = speech.SpeechClient()
            logger.info("Google Cloud Speech クライアントを初期化しました")
            
        except Exception as e:
            logger.error(f"クライアント初期化エラー: {e}")
            raise
    
    def validate_audio_file(self, file_path: str) -> Dict[str, Any]:
        """
        音声ファイルの検証
        
        Args:
            file_path: 音声ファイルのパス
            
        Returns:
            検証結果の辞書
        """
        result = {
            'valid': False,
            'error': None,
            'file_size_mb': 0,
            'duration_seconds': 0
        }
        
        try:
            # ファイルの存在確認
            if not os.path.exists(file_path):
                result['error'] = "ファイルが存在しません"
                return result
            
            # ファイルサイズの確認
            file_size = os.path.getsize(file_path)
            file_size_mb = file_size / (1024 * 1024)
            result['file_size_mb'] = file_size_mb
            
            if file_size_mb > MAX_AUDIO_SIZE_MB:
                result['error'] = f"ファイルサイズが大きすぎます（最大{MAX_AUDIO_SIZE_MB}MB）"
                return result
            
            # ファイル拡張子の確認
            file_extension = os.path.splitext(file_path)[1].lower().lstrip('.')
            logger.info(f"ファイル拡張子: '{file_extension}'")
            if file_extension not in SUPPORTED_AUDIO_FORMATS:
                result['error'] = f"サポートされていないファイル形式です（対応形式: {', '.join(SUPPORTED_AUDIO_FORMATS)}）"
                logger.error(f"ファイル拡張子 '{file_extension}' がサポートされていません")
                return result
            
            result['valid'] = True
            logger.info(f"音声ファイル検証成功: {file_path}")
            
        except Exception as e:
            result['error'] = f"ファイル検証エラー: {e}"
            logger.error(f"ファイル検証エラー: {e}")
        
        return result
    
    def transcribe_audio(self, file_path: str) -> Dict[str, Any]:
        """
        音声ファイルをテキストに変換
        
        Args:
            file_path: 音声ファイルのパス
            
        Returns:
            変換結果の辞書
        """
        result = {
            'success': False,
            'text': '',
            'confidence': 0.0,
            'error': None,
            'word_count': 0
        }
        
        try:
            # ファイル検証
            validation = self.validate_audio_file(file_path)
            if not validation['valid']:
                result['error'] = validation['error']
                return result
            
            # 全てのファイルをモノラル、16000HzのWAVに変換（オプション）
            actual_file_path = file_path
            logger.info(f"音声ファイルを変換中: {file_path}")
            converted_file = convert_to_wav(file_path)
            if converted_file != file_path:
                actual_file_path = converted_file
                logger.info(f"変換完了: {actual_file_path}")
            else:
                logger.info("元のファイルを使用します")
            
            # 音声ファイルの読み込み
            with io.open(actual_file_path, 'rb') as audio_file:
                content = audio_file.read()
            
            # 音声認識の実行（長時間音声対応）
            audio = RecognitionAudio(content=content)
            
            # 設定を更新（ENCODING_UNSPECIFIEDで自動判定、sample_rate_hertzも自動判定）
            config_dict = dict(SPEECH_CONFIG)
            config_dict['encoding'] = 'ENCODING_UNSPECIFIED'  # 自動判定
            # sample_rate_hertzは省略してAPIが自動判定
            if 'sample_rate_hertz' in config_dict:
                del config_dict['sample_rate_hertz']
            config = RecognitionConfig(**config_dict)
            
            logger.info(f"音声認識を開始: {actual_file_path} (LINEAR16, モノラル, 16000Hz)")
            
            # ファイルサイズをチェック
            content_size_mb = len(content) / (1024 * 1024)
            logger.info(f"音声ファイルサイズ: {content_size_mb:.2f}MB")
            
            # すべてのファイルで通常認識を試行し、失敗した場合に非同期APIを使用
            if False:  # 自動判定をスキップ
                logger.info("大容量ファイルのため非同期認識を開始...")
                operation = self.client.long_running_recognize(config=config, audio=audio)
                
                # 完了を待つ
                logger.info("音声認識処理中...")
                response = operation.result(timeout=300)  # 5分のタイムアウト
                
                # 結果の処理
                if response.results:
                    # 全ての結果を結合
                    transcripts = []
                    for res in response.results:
                        transcripts.append(res.alternatives[0].transcript)
                    
                    result['text'] = ' '.join(transcripts)
                    result['confidence'] = sum(res.alternatives[0].confidence for res in response.results if res.alternatives[0].confidence) / len(response.results)
                    result['success'] = True
                    result['word_count'] = len(result['text'].split())
                    
                    logger.info(f"長時間音声認識完了: {result['word_count']}語, 平均信頼度: {result['confidence']:.2f}")
                else:
                    result['error'] = "音声認識の結果がありません"
                    logger.warning("音声認識の結果がありません")
            else:
                try:
                    # 通常の認識を試行
                    response = self.client.recognize(config=config, audio=audio)
                    
                    # 結果の処理
                    if response.results:
                        # 最も信頼度の高い結果を取得
                        best_result = max(response.results, key=lambda x: x.alternatives[0].confidence)
                        result['text'] = best_result.alternatives[0].transcript
                        result['confidence'] = best_result.alternatives[0].confidence
                        result['success'] = True
                        result['word_count'] = len(result['text'].split())
                        
                        logger.info(f"音声認識完了: {result['word_count']}語, 信頼度: {result['confidence']:.2f}")
                    else:
                        result['error'] = "音声認識の結果がありません"
                        logger.warning("音声認識の結果がありません")
                        
                except Exception as e:
                    # エラーが発生した場合は非同期APIを試行
                    if "too long" in str(e) or "LongRunningRecognize" in str(e) or "duration limit" in str(e) or "Inline audio exceeds" in str(e):
                        logger.info("長時間音声のためGCSを使用した非同期認識を開始...")
                        
                        try:
                            # GCSにファイルをアップロード
                            gcs_handler = GCSHandler()
                            gcs_uri = gcs_handler.upload_file(actual_file_path)
                            logger.info(f"ファイルをGCSにアップロードしました: {gcs_uri}")
                            
                            # GCS URIから音声認識
                            result = self.transcribe_audio_from_gcs(gcs_uri)
                            
                            # GCSからファイルを削除
                            import os
                            gcs_handler.delete_file(os.path.basename(actual_file_path))
                            
                        except Exception as gcs_error:
                            logger.error(f"GCS処理エラー: {gcs_error}")
                            result['error'] = f"GCS処理エラー: {gcs_error}"
                    else:
                        raise
                
        except Exception as e:
            result['error'] = f"音声認識エラー: {e}"
            logger.error(f"音声認識エラー: {e}")
        
        return result
    
    def transcribe_audio_from_bytes(self, audio_bytes: bytes, encoding: str = 'WEBM_OPUS') -> Dict[str, Any]:
        """
        バイトデータから音声をテキストに変換
        
        Args:
            audio_bytes: 音声データのバイト
            encoding: 音声エンコーディング
            
        Returns:
            変換結果の辞書
        """
        result = {
            'success': False,
            'text': '',
            'confidence': 0.0,
            'error': None,
            'word_count': 0
        }
        
        try:
            # 音声認識の実行
            audio = RecognitionAudio(content=audio_bytes)
            config = RecognitionConfig(
                encoding=encoding,
                sample_rate_hertz=SPEECH_CONFIG['sample_rate_hertz'],
                language_code=SPEECH_CONFIG['language_code'],
                enable_automatic_punctuation=SPEECH_CONFIG['enable_automatic_punctuation'],
                enable_word_time_offsets=SPEECH_CONFIG['enable_word_time_offsets'],
                model=SPEECH_CONFIG['model']
            )
            
            logger.info("音声認識を開始（バイトデータ）")
            response = self.client.recognize(config=config, audio=audio)
            
            # 結果の処理
            if response.results:
                best_result = max(response.results, key=lambda x: x.alternatives[0].confidence)
                result['text'] = best_result.alternatives[0].transcript
                result['confidence'] = best_result.alternatives[0].confidence
                result['success'] = True
                result['word_count'] = len(result['text'].split())
                
                logger.info(f"音声認識完了: {result['word_count']}語, 信頼度: {result['confidence']:.2f}")
            else:
                result['error'] = "音声認識の結果がありません"
                logger.warning("音声認識の結果がありません")
                
        except Exception as e:
            result['error'] = f"音声認識エラー: {e}"
            logger.error(f"音声認識エラー: {e}")
        
        return result

    def transcribe_audio_from_gcs(self, gcs_uri: str) -> Dict[str, Any]:
        """
        GCS URIから音声をテキストに変換（長時間音声対応）
        
        Args:
            gcs_uri: Google Cloud Storage のURI (例: gs://bucket-name/file.wav)
            
        Returns:
            変換結果の辞書
        """
        result = {
            'success': False,
            'text': '',
            'confidence': 0.0,
            'error': None,
            'word_count': 0
        }
        
        try:
            # GCS URI を使用して音声認識を実行
            audio = RecognitionAudio(uri=gcs_uri)
            
            # 設定を更新
            config_dict = dict(SPEECH_CONFIG)
            config_dict['encoding'] = 'ENCODING_UNSPECIFIED'
            if 'sample_rate_hertz' in config_dict:
                del config_dict['sample_rate_hertz']
            config = RecognitionConfig(**config_dict)
            
            logger.info(f"GCS URIから音声認識を開始: {gcs_uri}")
            
            # 非同期APIを使用（長時間音声対応）
            operation = self.client.long_running_recognize(config=config, audio=audio)
            
            # 完了を待つ
            logger.info("音声認識処理中（長時間音声）...")
            response = operation.result(timeout=600)  # 10分のタイムアウト
            
            # 結果の処理
            if response.results:
                # 全ての結果を結合
                transcripts = []
                confidences = []
                for res in response.results:
                    transcripts.append(res.alternatives[0].transcript)
                    confidences.append(res.alternatives[0].confidence)
                
                result['text'] = ' '.join(transcripts)
                result['confidence'] = sum(confidences) / len(confidences)
                result['success'] = True
                result['word_count'] = len(result['text'].split())
                
                logger.info(f"長時間音声認識完了: {result['word_count']}語, 平均信頼度: {result['confidence']:.2f}")
            else:
                result['error'] = "音声認識の結果がありません"
                logger.warning("音声認識の結果がありません")
                
        except Exception as e:
            result['error'] = f"音声認識エラー: {e}"
            logger.error(f"音声認識エラー: {e}")
        
        return result


def create_voice_recognizer(credentials_path: Optional[str] = None) -> VoiceRecognizer:
    """
    音声認識オブジェクトを作成
    
    Args:
        credentials_path: Google Cloud認証情報のパス
        
    Returns:
        VoiceRecognizerインスタンス
    """
    return VoiceRecognizer(credentials_path)


# テスト用の関数
def test_voice_recognition(file_path: str, credentials_path: Optional[str] = None):
    """
    音声認識のテスト関数
    
    Args:
        file_path: テスト用音声ファイルのパス
        credentials_path: Google Cloud認証情報のパス
    """
    try:
        recognizer = create_voice_recognizer(credentials_path)
        result = recognizer.transcribe_audio(file_path)
        
        print("=== 音声認識テスト結果 ===")
        print(f"成功: {result['success']}")
        print(f"テキスト: {result['text']}")
        print(f"信頼度: {result['confidence']:.2f}")
        print(f"語数: {result['word_count']}")
        if result['error']:
            print(f"エラー: {result['error']}")
            
    except Exception as e:
        print(f"テストエラー: {e}")


if __name__ == "__main__":
    # テスト実行例
    test_file = "test_audio.wav"  # テスト用音声ファイル
    credentials = "configs/service-account-key.json"  # 認証情報ファイル
    
    if os.path.exists(test_file):
        test_voice_recognition(test_file, credentials)
    else:
        print(f"テストファイルが見つかりません: {test_file}")
