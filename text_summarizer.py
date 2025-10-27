"""
テキスト要約機能のメインモジュール
ChatGPT APIを使用してテキストを要約・構造化
"""

import logging
from typing import Optional, Dict, Any
from openai import OpenAI
from config import OPENAI_API_KEY

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TextSummarizer:
    """テキスト要約クラス"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初期化
        
        Args:
            api_key: OpenAI APIキー
        """
        self.api_key = api_key or OPENAI_API_KEY
        
        if not self.api_key:
            raise ValueError("OpenAI APIキーが設定されていません")
        
        self.client = OpenAI(api_key=self.api_key)
        logger.info("TextSummarizerを初期化しました")
    
    def summarize_text(self, text: str) -> Dict[str, Any]:
        """
        テキストを要約
        
        Args:
            text: 要約するテキスト
            
        Returns:
            要約結果の辞書
        """
        result = {
            'success': False,
            'summary': '',
            'error': None
        }
        
        try:
            # プロンプトの作成
            prompt = self._create_summary_prompt(text)
            
            # ChatGPT APIを呼び出し（新APIに対応）
            response = self.client.chat.completions.create(
                model="gpt-4o",  # より高精度なモデルに変更
                messages=[
                    {"role": "system", "content": "あなたは建設業界の音声議事録を正確に要約する専門家です。建設業界の専門用語や業務内容を理解し、適切に分類します。測量・設計業務における数値や単位（面積、距離、角度、座標など）を正確に認識し、記載することが重要です。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,  # より安定した出力のために温度を下げる
                max_tokens=2000
            )
            
            result['summary'] = response.choices[0].message.content
            result['success'] = True
            logger.info("テキストの要約が完了しました")
            
        except Exception as e:
            result['error'] = f"要約エラー: {e}"
            logger.error(f"要約エラー: {e}")
        
        return result
    
    def _create_summary_prompt(self, text: str) -> str:
        """
        要約用のプロンプトを作成
        
        Args:
            text: 要約するテキスト
            
        Returns:
            プロンプト
        """
        prompt = f"""以下の音声内容を建設業界の業務報告書として要約し、指定の形式で出力してください。

【出力形式】
1. 業務内容
   ※音声内で業務名（プロジェクト名、案件名など）が言及されている場合は、業務内容の冒頭に記載してください
   
   ※測定業務、設計業務、地質業務のうち、実際に行われた業務のみを記載してください。番号は1から連番で割り当ててください
   （例：測定業務がない場合は、設計業務を(2)ではなく(1)として記載）
   
   (1) 測量業務（実際に行われた場合のみ）
   1)現地測量を実施し、面積2.5㎢の測量を完了した
   2)基準点5点を設置し、座標を測定した（X座標:12345.67、Y座標:67890.12、標高:45.3m）
   
   (2) 設計業務（実際に行われた場合のみ）
   1)平面図を作成し、敷地面積3500㎡の建物設計を実施した
   2)立面図を作成し、建物高さ15.5m、延べ面積850㎡の設計を行った
   
   (3) 地質業務（実際に行われた場合のみ）
   1)具体的な作業内容1
   2)具体的な作業内容2
   
   (4) その他（実際に行われた場合のみ）
   1)具体的な作業内容1
   2)具体的な作業内容2

2. 提出書類
以下の書類を2部提出した。
具体的な書類名を列挙

ー以上ー

【音声内容】
{text}

【重要な指示】
1. 音声内容の**すべての重要な情報**を漏れなく抽出してください
2. 音声内で業務名（プロジェクト名、案件名、工事名など）が言及されている場合は、業務内容の冒頭に明記してください
3. 音声内容が短い場合や、業務内容が不明確な場合は、音声に含まれる情報を可能な限り抽出し、「その他」カテゴリに記述してください
4. 業務内容は以下の基準で分類してください：
   - 測量業務：測量、現地調査、測量点の設置、座標測定など
   - 設計業務：図面作成、設計検討、CAD作業、図面修正など
   - 地質業務：ボーリング調査、土質調査、地盤調査、地質分析など
   - その他：上記に該当しない作業（会議、打ち合わせ、書類準備、出張、移動など）
5. **番号の付け方**：測定業務、設計業務、地質業務、その他のうち、実際に行われた業務のみを記載し、番号は(1)から連番で割り当ててください。存在しない業務の番号は飛ばさず、連番で記載してください（例：測定業務がない場合は、設計業務を(1)として記載）
6. 各項目は**具体的な作業内容**として記述してください
7. 文章は常体（だ・である調）で記述してください
8. **測量・設計関連の数値と単位を正確に記載してください**：
   - 面積の単位（㎡、㎢、ヘクタール等）
   - 距離の単位（m、km、mm等）
   - 角度の単位（度、分、秒等）
   - 座標値（X座標、Y座標、標高など）
   - 数量（点、箇所、個等）
   - これらの単位や数値は音声内で言及されていれば必ず正確に記載してください
9. 作業の時間、数量、場所などの具体的な情報があれば必ず含めてください
10. 項目がないカテゴリは出力しないでください（空欄にせず、そのカテゴリ自体を省略）
11. 提出書類については、音声内で言及されている書類名があればそれを記載し、なければ空白にしてください
12. **重要な注意**：音声内容が業務に関連しない一般的な会話（例：「今広島にいます」）の場合でも、その情報を「その他」カテゴリに記述してください

上記の形式と指示に従って、音声内容を正確に要約してください。"""
        
        return prompt


def create_text_summarizer(api_key: Optional[str] = None) -> TextSummarizer:
    """
    テキスト要約オブジェクトを作成
    
    Args:
        api_key: OpenAI APIキー
        
    Returns:
        TextSummarizerインスタンス
    """
    return TextSummarizer(api_key)


# テスト用の関数
def test_text_summarization(text: str, api_key: Optional[str] = None):
    """
    テキスト要約のテスト関数
    
    Args:
        text: テスト用テキスト
        api_key: OpenAI APIキー
    """
    try:
        summarizer = create_text_summarizer(api_key)
        result = summarizer.summarize_text(text)
        
        print("=== テキスト要約テスト結果 ===")
        print(f"成功: {result['success']}")
        print(f"\n要約内容:")
        print(result['summary'])
        if result['error']:
            print(f"\nエラー: {result['error']}")
            
    except Exception as e:
        print(f"テストエラー: {e}")


if __name__ == "__main__":
    # テスト実行例
    test_text = """
    本日は測量業務について進めました。
    まず、近隣の状況を確認し、現地測量を実施しました。
    設計業務としては、平面図と立面図を作成しました。
    地質調査では、ボーリング調査を行い、土質状況を確認しました。
    その他、必要な書類を準備しました。
    """
    
    test_text_summarization(test_text, OPENAI_API_KEY)
