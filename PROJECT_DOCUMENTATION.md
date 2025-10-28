# 音声要約システム - 完全ドキュメント

## 📋 プロジェクト概要

### 目的
測量設計の業務で使用する音声データを自動で要約し、指定されたフォーマットで構造化された議事録を生成するWebアプリケーション。

### 主な機能
1. 音声ファイルのアップロード（WAV形式、モノラル推奨）
2. Google Cloud Speech-to-Text APIを使用した文字起こし
3. OpenAI GPT-4oを使用したテキスト要約
4. 指定フォーマットでの構造化された議事録生成
5. クラウドデプロイ（Render）によるオンラインアクセス
6. モバイル対応・PWA対応

---

## 🏗️ アーキテクチャ

### 技術スタック
```
フロントエンド: HTML/CSS/JavaScript
バックエンド: Python (Flask)
音声認識: Google Cloud Speech-to-Text API
テキスト要約: OpenAI GPT-4o API
ストレージ: Google Cloud Storage (長時間音声対応)
デプロイ: Render.com
```

### ディレクトリ構造
```
voice_summary_system/
├── app.py                      # Flaskメインアプリケーション
├── config.py                   # 設定管理
├── convert_audio.py            # 音声変換（FFmpeg）
├── voice_recognizer.py         # 音声認識（Google Cloud）
├── text_summarizer.py          # テキスト要約（OpenAI）
├── formatter.py                # フォーマット構造化
├── gcs_handler.py              # GCS統合
├── requirements.txt             # 依存パッケージ
├── Procfile                    # Render起動コマンド
├── templates/
│   └── index.html              # メインHTML
├── static/
│   ├── style.css               # スタイル
│   ├── manifest.json           # PWA設定
│   ├── icon-192.png            # PWAアイコン
│   └── icon-512.png            # PWAアイコン
├── configs/
│   └── service-account-key.json # Google Cloud認証情報
├── uploads/                    # アップロードファイル保存先
└── outputs/                    # 生成結果保存先
```

---

## 🔧 設定ファイル

### config.py
```python
# 環境変数から設定を取得
GOOGLE_APPLICATION_CREDENTIALS_JSON = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME', 'voice-summary-audio')
```

### 環境変数（Render）
```
OPENAI_API_KEY: OpenAI APIキー
GOOGLE_APPLICATION_CREDENTIALS_JSON: Google Cloud認証情報（JSON形式）
GCS_BUCKET_NAME: voice-summary-audio
FLASK_ENV: production
FLASK_DEBUG: False
PORT: 10000
```

---

## 🚀 デプロイ状態

### 現在のデプロイ
- **プラットフォーム**: Render.com
- **URL**: https://voice-summary-system.onrender.com
- **プラン**: Free（無料）
- **制限**: 15分非アクティブで停止、再起動に約30-50秒

### GitHub
- **リポジトリ**: https://github.com/tale555/voice-summary-system
- **ブランチ**: main
- **最新コミット**: Fix OpenAI SDK version compatibility

---

## 📝 API仕様

### エンドポイント

#### POST /upload
音声ファイルをアップロードして処理を開始

**リクエスト:**
- Content-Type: multipart/form-data
- file: 音声ファイル（WAV形式推奨）

**レスポンス:**
```json
{
  "success": true,
  "transcript": "文字起こしテキスト",
  "summary": {
    "1. 業務内容": {
      "(1) 測量業務": ["...", "..."]
    }
  }
}
```

---

## 🎯 主な処理フロー

### 1. 音声アップロード
```
ユーザー → ブラウザ → Flaskアプリ → uploads/ディレクトリ
```

### 2. 音声認識
```
FFmpeg → WAV変換（モノラル）
→ Google Cloud Speech-to-Text API → テキスト取得
```

### 3. テキスト要約
```
テキスト → OpenAI GPT-4o API → 構造化された要約
```

### 4. 結果表示
```
要約 → ブラウザ → ダウンロード可能
```

---

## 📦 依存パッケージ

### requirements.txt
```
Flask==2.3.3
google-cloud-speech==2.21.0
google-cloud-storage==2.10.0
openai>=1.12.0
python-dotenv==1.0.0
Werkzeug==2.3.7
gunicorn==21.2.0
pydub==0.25.1
ffmpeg-python==0.2.0
```

---

## 🔐 セキュリティ

### APIキー保護
- 環境変数として管理（Renderのシークレット機能）
- GitHubにはプッシュしない（.gitignore設定済み）
- 本番環境では非公開設定を維持

### ファイルアップロード制限
- 最大100MB
- WAV形式推奨（モノラル）

---

## 💰 料金情報

### Render（無料プラン）
- **費用**: $0/月
- **制限**: 15分非アクティブで停止
- **リソース**: 512MB RAM, 0.1 CPU

### Google Cloud Speech-to-Text
- **無料枠**: 60分/月（毎月リセット）
- **超過**: 従量課金
- **現在**: 課金アカウント設定済み

### OpenAI API
- **従量課金制**
- **モデル**: gpt-4o
- **現在**: 課金アカウント設定済み

**月額目安**: 数百円〜1,000円程度（利用量による）

---

## 🎨 主要なファイルの説明

### app.py
Flaskメインアプリケーション。ルーティング、ファイルアップロード処理、エラーハンドリングを担当。

### convert_audio.py
FFmpegを使用した音声ファイル変換。ステレオ→モノラル、MP3/M4A→WAV変換を実施。

### voice_recognizer.py
Google Cloud Speech-to-Text APIとの統合。ローカルファイル処理と長時間音声対応（GCS経由）。

### text_summarizer.py
OpenAI GPT-4o APIとの統合。テキスト要約と構造化処理を実行。

### formatter.py
指定フォーマットに従って要約を構造化。測量設計業務用の議事録形式に対応。

### gcs_handler.py
Google Cloud Storage統合。長時間音声ファイルの一時保存とSpeech-to-Text APIへの送信を管理。

---

## 🐛 トラブルシューティング

### よくある問題

#### 1. 音声認識エラー
- **原因**: ステレオ音声
- **解決**: FFmpegでモノラル変換

#### 2. OpenAI APIエラー
- **原因**: 古いSDKバージョン
- **解決**: openai>=1.12.0に更新

#### 3. Renderデプロイ失敗
- **原因**: 環境変数未設定
- **解決**: Renderの「Environment」タブで設定確認

---

## 📊 テスト結果

### 実証済み
- ✅ 音声認識（Google Cloud Speech-to-Text）
- ✅ テキスト要約（OpenAI GPT-4o）
- ✅ フォーマット構造化
- ✅ クラウドデプロイ（Render）
- ✅ モバイル対応
- ✅ PWA対応

### テスト実行日
2025年10月28日

### テストデータ
- ファイル名: 無題1.wav
- サイズ: 15.73 MB
- 内容: 測量設計の業務計画書読み合わせ

---

## 🔄 今後の改善案

### 機能追加
- [ ] 複数ファイルの一括処理
- [ ] カスタムフォーマット選択
- [ ] 音声品質チェック機能
- [ ] 処理進捗の詳細表示

### パフォーマンス改善
- [ ] 非同期処理の導入
- [ ] キャッシュ機能の追加
- [ ] データベース連携

### セキュリティ強化
- [ ] ユーザー認証機能
- [ ] ファイル暗号化
- [ ] アクセスログ管理

---

## 📚 参考資料

### 公式ドキュメント
- [Flask公式ドキュメント](https://flask.palletsprojects.com/)
- [Google Cloud Speech-to-Text](https://cloud.google.com/speech-to-text/docs)
- [OpenAI API](https://platform.openai.com/docs)
- [Render.com](https://render.com/docs)

### 関連ファイル
- `README.md`: プロジェクト概要
- `SETUP_GUIDE.md`: セットアップ手順
- `TEST_GUIDE.md`: テスト手順
- `MOBILE_GUIDE.md`: モバイル使用方法
- `DEPLOYMENT_GUIDE.md`: デプロイ方法
- `GCS_SETUP.md`: Google Cloud Storage設定
- `FFMPEG_INSTALL.md`: FFmpegインストール手順

---

## 👥 開発情報

### 作成者
- GitHub: tale555

### プロジェクト期間
2025年10月

### 最終更新
2025年10月28日

---

## 📞 問い合わせ

問題が発生した場合は、GitHubリポジトリのIssuesで報告してください。

**リポジトリ**: https://github.com/tale555/voice-summary-system

