# GCS長時間音声認識テストガイド

このガイドでは、GCS統合による長時間音声（60秒超）の処理をテストする方法を説明します。

## 準備

### 1. 音声ファイルの用意

以下のいずれかを用意してください：
- **60秒超の音声ファイル**: WAV, MP3, M4Aなどの対応形式
- **テスト用の短い音声ファイル**: 動作確認用（60秒以内）

### 2. ファイルの配置

音声ファイルを以下のいずれかの場所に配置してください：
- `voice_summary_system/uploads/` フォルダ内
- `voice_summary_system/` フォルダ内

## テスト方法

### 方法1: コマンドラインテスト

1. **PowerShellまたはコマンドプロンプトを開く**

2. **voice_summary_systemフォルダに移動**
   ```powershell
   cd "C:\Users\mhero\OneDrive\デスクトップ\cursor練習\voice_summary_system"
   ```

3. **テストスクリプトを実行**
   ```powershell
   python test_gcs_voice.py <音声ファイルのパス>
   ```

   **例：**
   ```powershell
   # uploadsフォルダ内のファイルをテスト
   python test_gcs_voice.py uploads/test_audio.wav
   
   # または、現在のフォルダ内のファイルをテスト
   python test_gcs_voice.py test_audio.wav
   ```

### 方法2: Webインターフェースからテスト

1. **Flaskサーバーを起動**
   ```powershell
   cd "C:\Users\mhero\OneDrive\デスクトップ\cursor練習\voice_summary_system"
   python app.py
   ```

2. **ブラウザでアクセス**
   - http://127.0.0.1:5000 にアクセス

3. **音声ファイルをアップロード**
   - 「ファイルを選択」をクリック
   - 60秒超の音声ファイルを選択
   - 「アップロード」をクリック

4. **結果を確認**
   - 処理が完了すると、結果が表示されます
   - ログに「GCS URIから音声認識を開始」と表示されればGCS経由で処理されています

## 期待される動作

### 60秒以内の音声ファイル

```
音声認識を開始: (ファイルパス) (LINEAR16, モノラル, 16000Hz)
音声ファイルサイズ: X.XXMB
音声認識完了: XX語, 信頼度: 0.XX
```

**GCSは使用されません（直接処理）**

### 60秒超の音声ファイル

```
音声認識を開始: (ファイルパス) (LINEAR16, モノラル, 16000Hz)
音声ファイルサイズ: X.XXMB
長時間音声のためGCSを使用した非同期認識を開始...
ファイルをGCSにアップロードしました: gs://voice-summary-audio/XXX.wav
GCS URIから音声認識を開始: gs://voice-summary-audio/XXX.wav
音声認識処理中（長時間音声）...
長時間音声認識完了: XXX語, 平均信頼度: 0.XX
GCSファイルを削除しました: XXX.wav
```

**GCS経由で処理されます**

## トラブルシューティング

### 「バケットが見つかりません」エラー

- `.env`ファイルの`GCS_BUCKET_NAME`が正しいか確認
- GCSバケットが作成されているか確認

### 「権限がありません」エラー

- サービスアカウントに「Storage オブジェクト管理者」のロールが付与されているか確認

### 「GCS処理エラー」が発生する場合

- GCSバケットが作成されているか確認
- サービスアカウントの権限を確認
- 認証情報ファイル（`configs/service-account-key.json`）が正しく設定されているか確認

## ログの確認

詳細なログを確認するには、Flaskサーバーを起動したターミナルを見てください。

正常な動作の場合、以下のようなログが表示されます：
```
INFO:voice_recognizer:音声認識を開始: ...
INFO:voice_recognizer:長時間音声のためGCSを使用した非同期認識を開始...
INFO:gcs_handler:ファイルをGCSにアップロードしました: gs://...
INFO:voice_recognizer:GCS URIから音声認識を開始: gs://...
INFO:voice_recognizer:長時間音声認識完了: XXX語, 平均信頼度: 0.XX
```
