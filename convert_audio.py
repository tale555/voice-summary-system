"""
音声ファイル変換モジュール
MP3等をWAV形式に変換
"""

import os
import logging
import subprocess
import tempfile

logger = logging.getLogger(__name__)

def convert_to_wav(input_file: str, output_file: str = None) -> str:
    """
    音声ファイルをWAV形式に変換（モノラル、16000Hzに変換）
    
    Args:
        input_file: 入力ファイルのパス
        output_file: 出力ファイルのパス（Noneの場合自動生成）
        
    Returns:
        変換後のファイルパス
    """
    if output_file is None:
        # 一時ファイルとして作成
        temp_dir = tempfile.gettempdir()
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(temp_dir, f"{base_name}.wav")
    
    try:
        # FFmpegを使用して直接変換
        logger.info(f"FFmpegを使用して変換開始: {input_file}")
        
        # FFmpegコマンド
        # -i: 入力ファイル
        # -ac 1: モノラル（1チャンネル）
        # -ar 16000: サンプリングレート16000Hz
        # -y: 出力ファイルを上書き
        cmd = [
            'ffmpeg',
            '-i', input_file,  # 入力ファイル
            '-ac', '1',        # モノラル
            '-ar', '16000',    # 16kHz
            '-y',              # 上書き
            output_file        # 出力ファイル
        ]
        
        logger.info(f"実行コマンド: {' '.join(cmd)}")
        
        # FFmpegを実行
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        logger.info(f"音声ファイルを変換しました: {input_file} -> {output_file}")
        logger.info(f"FFmpeg出力: {result.stderr}")
        return output_file
        
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg実行エラー: {e}")
        logger.error(f"FFmpegエラー出力: {e.stderr}")
        return input_file
    except FileNotFoundError:
        logger.error("FFmpegが見つかりません。FFmpegをインストールしてください")
        return input_file
    except Exception as e:
        logger.error(f"音声ファイル変換エラー: {e}。元のファイルを使用します")
        return input_file
