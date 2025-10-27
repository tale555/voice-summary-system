"""
音声要約システム - Flaskアプリケーション
"""

import os
import logging
from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
from voice_recognizer import create_voice_recognizer
from text_summarizer import create_text_summarizer
from formatter import create_formatter
from config import (
    GOOGLE_APPLICATION_CREDENTIALS,
    OPENAI_API_KEY,
    UPLOAD_FOLDER,
    MAX_CONTENT_LENGTH
)

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flaskアプリケーション作成
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['SECRET_KEY'] = 'your-secret-key-here'

# 必要なディレクトリを作成
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('outputs', exist_ok=True)


@app.route('/')
def index():
    """ホームページ"""
    return render_template('index.html')


@app.route('/manifest.json')
def manifest():
    """PWAマニフェストファイル"""
    return send_file('static/manifest.json', mimetype='application/json')


@app.route('/upload', methods=['POST'])
def upload_file():
    """ファイルアップロードと処理"""
    try:
        # ファイルの確認
        if 'file' not in request.files:
            return jsonify({'error': 'ファイルが選択されていません'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'ファイルが選択されていません'}), 400
        
        # ファイルを保存（日本語ファイル名に対応）
        # 元のファイル名から拡張子を取得
        original_filename = file.filename
        file_ext = os.path.splitext(original_filename)[1] if '.' in original_filename else ''
        
        # 安全なファイル名を生成（タイムスタンプを使用）
        import datetime
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        filename = f"audio_{timestamp}{file_ext}" if file_ext else f"audio_{timestamp}"
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        logger.info(f"ファイルがアップロードされました: {original_filename} -> {filename}")
        
        # 音声認識
        logger.info("音声認識を開始...")
        recognizer = create_voice_recognizer(GOOGLE_APPLICATION_CREDENTIALS)
        speech_result = recognizer.transcribe_audio(filepath)
        
        if not speech_result['success']:
            return jsonify({'error': f"音声認識エラー: {speech_result['error']}"}), 500
        
        transcript = speech_result['text']
        logger.info(f"音声認識完了: {speech_result['word_count']}語")
        
        # テキスト要約
        logger.info("テキスト要約を開始...")
        summarizer = create_text_summarizer(OPENAI_API_KEY)
        summary_result = summarizer.summarize_text(transcript)
        
        if not summary_result['success']:
            return jsonify({'error': f"要約エラー: {summary_result['error']}"}), 500
        
        summary_text = summary_result['summary']
        logger.info("テキスト要約完了")
        
        # フォーマット整形
        logger.info("フォーマット整形を開始...")
        formatter = create_formatter()
        format_result = formatter.format_summary(summary_text)
        
        if not format_result['success']:
            formatted_text = summary_text  # 整形に失敗した場合は元のテキストを使用
            logger.warning("フォーマット整形に失敗しました")
        else:
            formatted_text = format_result['formatted_text']
            logger.info("フォーマット整形完了")
        
        # 結果をファイルに保存
        # ファイル名から拡張子を取得（拡張子がない場合はそのまま使用）
        if '.' in filename:
            base_name = filename.rsplit('.', 1)[0]
        else:
            base_name = filename
        output_filename = base_name + '_summary.txt'
        output_filepath = os.path.join('outputs', output_filename)
        
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(f"【音声ファイル】: {filename}\n")
            f.write(f"【音声認識結果】\n{transcript}\n\n")
            f.write(f"【要約結果】\n{formatted_text}\n")
        
        return jsonify({
            'success': True,
            'transcript': transcript,
            'summary': formatted_text,
            'output_file': output_filename
        })
        
    except Exception as e:
        logger.error(f"エラー: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/download/<filename>')
def download_file(filename):
    """ファイルダウンロード"""
    try:
        filepath = os.path.join('outputs', secure_filename(filename))
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        else:
            return jsonify({'error': 'ファイルが見つかりません'}), 404
    except Exception as e:
        logger.error(f"ダウンロードエラー: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # ポート番号を環境変数から取得（Railway対応）
    port = int(os.getenv('PORT', 5000))
    
    # 開発環境か本番環境かを判定
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # 開発サーバーの起動
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
