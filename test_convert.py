"""
音声ファイル変換のテスト
"""

import sys
from convert_audio import convert_to_wav
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    # テスト用の音声ファイルパス
    if len(sys.argv) > 1:
        test_file = sys.argv[1]
    else:
        print("使用方法: python test_convert.py <音声ファイルのパス>")
        sys.exit(1)
    
    print(f"音声ファイルを変換中: {test_file}")
    result = convert_to_wav(test_file)
    
    if result != test_file:
        print(f"✓ 変換成功: {result}")
    else:
        print("✗ 変換が実行されませんでした")
        print("元のファイルが返されました")
