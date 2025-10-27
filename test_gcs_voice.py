"""
GCS長時間音声認識のテストスクリプト
長時間音声ファイル（60秒超）の処理をテストします
"""

import os
import sys
from voice_recognizer import create_voice_recognizer
from config import GOOGLE_APPLICATION_CREDENTIALS

def test_gcs_voice_recognition(file_path: str):
    """
    GCSを使用した長時間音声認識のテスト
    
    Args:
        file_path: テスト用の音声ファイルのパス
    """
    print("=== GCS長時間音声認識テスト ===\n")
    
    # ファイルの存在確認
    if not os.path.exists(file_path):
        print(f"❌ エラー: ファイルが見つかりません: {file_path}")
        return
    
    # ファイルサイズの確認
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    print(f"ファイル: {file_path}")
    print(f"ファイルサイズ: {file_size_mb:.2f}MB\n")
    
    try:
        # 音声認識オブジェクトを作成
        print("音声認識オブジェクトを作成中...")
        recognizer = create_voice_recognizer(GOOGLE_APPLICATION_CREDENTIALS)
        print("✓ 音声認識オブジェクトの作成が完了しました\n")
        
        # 音声認識を実行
        print("音声認識を開始します...")
        print("（長時間音声の場合はGCS経由で処理されます）\n")
        
        result = recognizer.transcribe_audio(file_path)
        
        # 結果を表示
        print("\n=== 音声認識結果 ===")
        print(f"成功: {'✓' if result['success'] else '✗'}")
        
        if result['success']:
            print(f"テキスト: {result['text']}")
            print(f"信頼度: {result['confidence']:.2f}")
            print(f"語数: {result['word_count']}語")
        else:
            print(f"エラー: {result['error']}")
        
        return result
        
    except Exception as e:
        print(f"❌ テストエラー: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    # コマンドライン引数からファイルパスを取得
    if len(sys.argv) > 1:
        test_file = sys.argv[1]
    else:
        print("使用方法: python test_gcs_voice.py <音声ファイルのパス>")
        print("\n例:")
        print("  python test_gcs_voice.py test_audio.wav")
        print("  python test_gcs_voice.py uploads/long_audio.mp3")
        sys.exit(1)
    
    # テスト実行
    test_gcs_voice_recognition(test_file)
