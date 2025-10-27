"""
フォーマット構造化機能のメインモジュール
要約結果を指定フォーマットに整形
"""

import re
import logging
from typing import Dict, Any, List, Optional

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TextFormatter:
    """テキスト整形クラス"""
    
    def __init__(self):
        """初期化"""
        self.sections = {
            'business_content': {
                'title': '1. 業務内容',
                'subsections': {
                    'survey': '(1) 測量業務',
                    'design': '(2) 設計業務',
                    'geology': '(3) 地質業務',
                    'other': '(4) その他'
                }
            },
            'documents': {
                'title': '2. 提出書類'
            },
            'end': 'ー以上ー'
        }
    
    def format_summary(self, summary_text: str) -> Dict[str, Any]:
        """
        要約テキストを構造化
        
        Args:
            summary_text: 要約テキスト
            
        Returns:
            構造化された結果
        """
        result = {
            'success': False,
            'formatted_text': '',
            'structured_data': {},
            'error': None
        }
        
        try:
            # テキストをパース
            parsed_data = self._parse_summary(summary_text)
            
            # 構造化されたデータをテキストに整形
            formatted_text = self._format_to_text(parsed_data)
            
            result['formatted_text'] = formatted_text
            result['structured_data'] = parsed_data
            result['success'] = True
            logger.info("テキストの整形が完了しました")
            
        except Exception as e:
            result['error'] = f"整形エラー: {e}"
            logger.error(f"整形エラー: {e}")
        
        return result
    
    def _parse_summary(self, text: str) -> Dict[str, Any]:
        """
        要約テキストをパース
        
        Args:
            text: 要約テキスト
            
        Returns:
            パースされたデータ
        """
        parsed = {
            'business_content': {
                'survey': [],
                'design': [],
                'geology': [],
                'other': []
            },
            'documents': '',
            'end': ''
        }
        
        # 業務内容の抽出
        business_match = re.search(r'1\.\s*業務内容(.*?)(?=2\.|ー以上|$)', text, re.DOTALL)
        if business_match:
            business_content = business_match.group(1)
            
            # 各業務項目を抽出
            parsed['business_content']['survey'] = self._extract_subsection(business_content, r'\(1\)\s*測量業務')
            parsed['business_content']['design'] = self._extract_subsection(business_content, r'\(2\)\s*設計業務')
            parsed['business_content']['geology'] = self._extract_subsection(business_content, r'\(3\)\s*地質業務')
            parsed['business_content']['other'] = self._extract_subsection(business_content, r'\(4\)\s*その他')
        
        # 提出書類の抽出
        documents_match = re.search(r'2\.\s*提出書類(.*?)(?=ー以上|$)', text, re.DOTALL)
        if documents_match:
            parsed['documents'] = documents_match.group(1).strip()
        
        # ー以上ーの確認
        if 'ー以上ー' in text or '以上' in text:
            parsed['end'] = 'ー以上ー'
        
        return parsed
    
    def _extract_subsection(self, text: str, pattern: str) -> List[str]:
        """
        サブセクションの項目を抽出
        
        Args:
            text: テキスト
            pattern: パターン
            
        Returns:
            項目のリスト
        """
        items = []
        
        # サブセクションを見つける
        match = re.search(pattern + r'(.*?)(?=\(|$)', text, re.DOTALL)
        if match:
            subsection_text = match.group(1)
            
            # 番号付き項目を抽出
            numbered_items = re.findall(r'\d+\)\s*([^\n]+)', subsection_text)
            items.extend([item.strip() for item in numbered_items])
            
            # ハイフン付き項目を抽出
            dash_items = re.findall(r'-\s*([^\n]+)', subsection_text)
            items.extend([item.strip() for item in dash_items])
        
        return items
    
    def _format_to_text(self, data: Dict[str, Any]) -> str:
        """
        構造化されたデータをテキストに整形
        
        Args:
            data: 構造化されたデータ
            
        Returns:
            整形されたテキスト
        """
        lines = []
        
        # 1. 業務内容
        lines.append(self.sections['business_content']['title'])
        
        # (1) 測量業務
        if data['business_content']['survey']:
            lines.append(f"   {self.sections['business_content']['subsections']['survey']}")
            for i, item in enumerate(data['business_content']['survey'], 1):
                if item:  # 空でない場合のみ追加
                    lines.append(f"  {i}) {item}")
        
        # (2) 設計業務
        if data['business_content']['design']:
            lines.append(f"   {self.sections['business_content']['subsections']['design']}")
            for i, item in enumerate(data['business_content']['design'], 1):
                if item:  # 空でない場合のみ追加
                    lines.append(f"  {i}) {item}")
        
        # (3) 地質業務
        if data['business_content']['geology']:
            lines.append(f"   {self.sections['business_content']['subsections']['geology']}")
            for i, item in enumerate(data['business_content']['geology'], 1):
                if item:  # 空でない場合のみ追加
                    lines.append(f"  {i}) {item}")
        
        # (4) その他
        if data['business_content']['other']:
            lines.append(f"   {self.sections['business_content']['subsections']['other']}")
            for i, item in enumerate(data['business_content']['other'], 1):
                if item:  # 空でない場合のみ追加
                    lines.append(f"  {i}) {item}")
        
        # 2. 提出書類
        lines.append("")
        lines.append(self.sections['documents']['title'])
        if data['documents']:
            # 提出書類の内容を整形
            if not data['documents'].startswith('以下'):
                lines.append('以下の書類を2部提出した。')
            lines.append(data['documents'])
        
        # ー以上ー
        lines.append("")
        lines.append(self.sections['end'])
        
        return '\n'.join(lines)
    
    def format_for_display(self, text: str) -> str:
        """
        表示用に整形
        
        Args:
            text: 元のテキスト
            
        Returns:
            整形されたテキスト
        """
        # 基本的な整形処理
        formatted = text
        
        # 余分な空白を削除
        formatted = re.sub(r'\n{3,}', '\n\n', formatted)
        
        # 項目の番号を統一
        formatted = re.sub(r'(\d+)\)\s*', r'\1) ', formatted)
        
        return formatted


def create_formatter() -> TextFormatter:
    """
    フォーマッターオブジェクトを作成
    
    Returns:
        TextFormatterインスタンス
    """
    return TextFormatter()


# テスト用の関数
def test_formatting(summary_text: str):
    """
    整形機能のテスト関数
    
    Args:
        summary_text: テスト用要約テキスト
    """
    try:
        formatter = create_formatter()
        result = formatter.format_summary(summary_text)
        
        print("=== フォーマット整形テスト結果 ===")
        print(f"成功: {result['success']}")
        print(f"\n整形されたテキスト:")
        print(result['formatted_text'])
        
        if result['error']:
            print(f"\nエラー: {result['error']}")
            
    except Exception as e:
        print(f"テストエラー: {e}")


if __name__ == "__main__":
    # テスト実行例
    test_summary = """
1. 業務内容
   (1) 測量業務
   1) 現地測量を実施した
   2) 測量点の設置位置を決定した
   
   (2) 設計業務
   1) 平面図を作成した
   2) 立面図を作成した
   
   (3) 地質業務
   1) ボーリング調査を実施した
   
   (4) その他
   1) 必要な書類を準備した

2. 提出書類
以下の書類を2部提出した。
業務計画書、身分証明書交付申請書

ー以上ー
    """
    
    test_formatting(test_summary)
