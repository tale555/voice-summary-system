# Google Cloud Storage セットアップガイド

このシステムで長時間音声（60秒超）を処理するには、Google Cloud Storage（GCS）の設定が必要です。

## 概要

- **現在の制限**: 約60秒以内の音声ファイルのみ対応
- **GCS統合後**: 最大60分の音声ファイルに対応可能

## 必要な作業

### 1. GCSバケットの作成

方法A: 検索機能を使用（推奨）
1. [Google Cloud Console](https://console.cloud.google.com/)にアクセス
2. プロジェクトを選択（Speech-to-Text APIと同じプロジェクト）
3. 画面上部の検索ボックスに「Cloud Storage」と入力
4. 「Cloud Storage」→「バケット」を選択
5. 「バケットを作成」をクリック
6. バケット名を入力（例: `voice-summary-audio`）
7. リージョンを選択（Speech-to-Text APIと同じリージョン推奨）
8. デフォルトのストレージクラスを選択
9. 「作成」をクリック

※注：リージョンはバケット作成画面で選択します。「us (米国の複数のリージョン)」が選択されている場合はそのままで問題ありません。

**現在のバケット状態：**
- バケット名: voice-summary-audio ✓
- 場所: us (米国の複数のリージョン) ✓
- ストレージクラス: Standard ✓
- 公開アクセス: 非公開 ✓

このバケットは正常に作成されており、次のステップに進むことができます。

方法B: メニューから選択
1. [Google Cloud Console](https://console.cloud.google.com/)にアクセス
2. プロジェクトを選択（Speech-to-Text APIと同じプロジェクト）
3. 左側メニューをスクロールして「Storage」または「Cloud Storage」を探す
4. 「バケット」を選択
5. 「バケットを作成」をクリック
6. 以降は上記の方法Aの手順6-9と同じ

### 2. サービスアカウントへの権限付与

**手順：**
1. Google Cloud Consoleの画面上部の検索ボックスに「サービスアカウント」と入力
2. 「サービスアカウント」を選択
3. サービスアカウントの一覧から、Speech-to-Text API用のサービスアカウント（通常は `test-xxxx@xxxx.iam.gserviceaccount.com` のような形式）を選択
4. 「ロールを割り当てる」画面が表示されるので、「+ 別のロールを追加」をクリック
5. 「役割を選択」のドロップダウンメニューをクリックし、「Storage」と入力して検索
6. 「Storage オブジェクト管理者」を選択
7. 「保存」をクリック

**注意：** 新しいロールを作成する必要はありません。既存の「Storage オブジェクト管理者」ロールを選択してください。

### 3. 環境変数の設定

`.env` ファイルにGCSバケット名を追加：

```env
# Google Cloud Storage 設定
GCS_BUCKET_NAME=your-bucket-name
```

または、`env_example.txt`を参考に設定してください。

## 使用方法

GCS統合後は、自動的に以下が行われます：

1. **60秒超の音声ファイル**: GCSにアップロードし、長時間音声認識APIを使用
2. **60秒以内の音声ファイル**: 従来どおり直接処理

## 注意事項

- GCSバケットの作成には、Google Cloudアカウントでの料金が発生する場合があります
- ストレージ料金とデータ転送料金が発生します（通常は無料枠内）
- GCSにアップロードされたファイルは、処理後に自動的に削除されます

## トラブルシューティング

### 「バケットが見つかりません」エラー

- バケット名が正しいか確認
- サービスアカウントに適切な権限があるか確認

### 「権限がありません」エラー

- サービスアカウントに「Storage オブジェクト管理者」の役割が付与されているか確認

## 参考リンク

- [Google Cloud Storage ドキュメント](https://cloud.google.com/storage/docs)
- [Cloud Speech-to-Text 長時間音声](https://cloud.google.com/speech-to-text/docs/async-recognize)
