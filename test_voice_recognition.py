"""
音声認識機能のテストスクリプト
"""

import os
import sys
from voice_recognizer import test_voice_recognition, create_voice_recognizer

def main():
    """メイン関数"""
    print("=== 音声認識機能テスト ===")
    
    # 認証情報のパス
    credentials_path = "configs/service-account-key.json"
    
    # 認証情報ファイルの確認
    if not os.path.exists(credentials_path):
        print(f"❌ 認証情報ファイルが見つかりません: {credentials_path}")
        print("Google Cloud Consoleからサービスアカウントキーをダウンロードして、")
        print("configs/service-account-key.json として保存してください。")
        return
    
    print(f"✅ 認証情報ファイルを確認: {credentials_path}")
    
    # 音声認識オブジェクトの作成テスト
    try:
        recognizer = create_voice_recognizer(credentials_path)
        print("✅ 音声認識オブジェクトの作成に成功")
    except Exception as e:
        print(f"❌ 音声認識オブジェクトの作成に失敗: {e}")
        return
    
    # テスト用音声ファイルの確認
    test_files = [
        "test_audio.wav",
        "test_audio.mp3",
        "test_audio.m4a"
    ]
    
    test_file = None
    for file in test_files:
        if os.path.exists(file):
            test_file = file
            break
    
    if not test_file:
        print("❌ テスト用音声ファイルが見つかりません")
        print("以下のいずれかのファイルを用意してください:")
        for file in test_files:
            print(f"  - {file}")
        print("\n=== 音声認識オブジェクトの作成テストのみ実行 ===")
        print("✅ 音声認識機能の基本設定は正常です")
        print("音声ファイルを用意してから再度テストしてください")
        return
    
    print(f"✅ テスト用音声ファイルを確認: {test_file}")
    
    # 音声認識のテスト実行
    print("\n=== 音声認識テスト実行 ===")
    test_voice_recognition(test_file, credentials_path)

if __name__ == "__main__":
    main()
