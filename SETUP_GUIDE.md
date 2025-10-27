# 音声要約システム セットアップガイド

## 必要な準備

### 1. Google Cloud Speech-to-Text API の設定

#### ステップ1: Google Cloud Console にアクセス
1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 新しいプロジェクトを作成するか、既存のプロジェクトを選択

#### ステップ2: Speech-to-Text API を有効化
1. 左側のメニューから「APIとサービス」→「ライブラリ」を選択
2. 「Cloud Speech-to-Text API」を検索
3. 「有効にする」をクリック

#### ステップ3: サービスアカウントの作成
1. 左側のメニューから「IAMと管理」→「サービスアカウント」を選択
2. 「サービスアカウントを作成」をクリック
3. サービスアカウント名を入力（例：voice-summary-system）
4. 「作成して続行」をクリック
5. ロールに「Cloud Speech-to-Text API ユーザー」を追加
6. 「完了」をクリック

#### ステップ4: サービスアカウントキーのダウンロード
1. 作成したサービスアカウントをクリック
2. 「キー」タブを選択
3. 「鍵を追加」→「新しい鍵を作成」を選択
4. キーのタイプを「JSON」に設定
5. 「作成」をクリック
6. ダウンロードされたJSONファイルを `configs/service-account-key.json` として保存

### 2. OpenAI API の設定

#### ステップ1: OpenAI アカウントの作成
1. [OpenAI Platform](https://platform.openai.com/) にアクセス
2. アカウントを作成またはログイン

#### ステップ2: API キーの取得
1. 左側のメニューから「API keys」を選択
2. 「Create new secret key」をクリック
3. キー名を入力（例：voice-summary-system）
4. 「Create secret key」をクリック
5. 表示されたAPIキーをコピーして保存

### 3. 環境変数の設定

#### ステップ1: 環境変数ファイルの作成
1. `env_example.txt` をコピーして `.env` ファイルを作成
2. 以下の内容を設定：

```env
# Google Cloud Speech-to-Text API 設定
GOOGLE_APPLICATION_CREDENTIALS=configs/service-account-key.json

# OpenAI API 設定
OPENAI_API_KEY=your_openai_api_key_here

# Flask 設定
FLASK_ENV=development
FLASK_DEBUG=True
```

#### ステップ2: 実際の値を設定
- `GOOGLE_APPLICATION_CREDENTIALS`: サービスアカウントキーのパス
- `OPENAI_API_KEY`: 取得したOpenAI APIキー

### 4. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 5. 動作確認

#### 音声認識機能のテスト
```bash
python test_voice_recognition.py
```

## トラブルシューティング

### よくあるエラー

#### 1. 認証エラー
```
google.auth.exceptions.DefaultCredentialsError
```
**解決方法**: サービスアカウントキーのパスが正しいか確認

#### 2. API が有効になっていない
```
google.api_core.exceptions.PermissionDenied
```
**解決方法**: Google Cloud Console で Speech-to-Text API が有効になっているか確認

#### 3. 音声ファイルの形式エラー
```
Unsupported audio format
```
**解決方法**: サポートされている形式（wav, mp3, flac, ogg, m4a, webm）を使用

### サポートされている音声形式
- WAV
- MP3
- FLAC
- OGG
- M4A
- WEBM

### 推奨設定
- サンプルレート: 48kHz
- ビットレート: 128kbps以上
- チャンネル: モノラルまたはステレオ

## 次のステップ

音声認識機能のテストが成功したら、次のタスク（テキスト要約機能）に進みます。
