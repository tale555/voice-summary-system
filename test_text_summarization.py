"""
テキスト要約機能のテストスクリプト
"""

import os
import sys
from text_summarizer import test_text_summarization, create_text_summarizer

def main():
    """メイン関数"""
    print("=== テキスト要約機能テスト ===")
    
    # OpenAI API キーの確認
    from config import OPENAI_API_KEY
    
    if not OPENAI_API_KEY or OPENAI_API_KEY.startswith('your_'):
        print("❌ OpenAI APIキーが設定されていません")
        print("config.py でOPENAI_API_KEYを設定してください")
        return
    
    print(f"✅ OpenAI APIキーが設定されています")
    
    # テキスト要約オブジェクトの作成テスト
    try:
        summarizer = create_text_summarizer(OPENAI_API_KEY)
        print("✅ テキスト要約オブジェクトの作成に成功")
    except Exception as e:
        print(f"❌ テキスト要約オブジェクトの作成に失敗: {e}")
        return
    
    # テスト用テキスト
    test_text = """
    本日の会議内容を報告します。
    
    測量業務については、先週実施した現地測量の結果を確認しました。
    近隣の状況を詳しく調査し、測量点の設置位置を決定しました。
    
    設計業務については、基本設計図面の作成を進めています。
    平面図、立面図、断面図の作成に着手し、構造計算も実施しました。
    
    地質業務については、ボーリング調査を実施しました。
    深さ20メートルまで掘削し、各層の土質サンプルを採取しました。
    分析結果を基に、地盤の強度を評価しました。
    
    その他、来週の作業計画を確認し、必要な書類の準備を行いました。
    """
    
    print("\n=== テキスト要約テスト実行 ===")
    test_text_summarization(test_text, OPENAI_API_KEY)

if __name__ == "__main__":
    main()
