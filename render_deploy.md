# Renderでデプロイする方法

音声要約システムをRenderにデプロイする手順です。

## 📋 事前準備

1. ✅ GitHubリポジトリにコードがプッシュされていること
2. ✅ Renderアカウントの作成

---

## 🚀 手順1: Renderに登録

### 1-1. Renderアカウントを作成

1. https://render.com にアクセス
2. 「Get Started for Free」をクリック
3. 「Continue with GitHub」を選択
4. GitHub認証を許可

---

## 🎯 手順2: Webサービスを作成

### 2-1. 新しいWebサービスを作成

1. Renderダッシュボードで「+ New」をクリック
2. 「Web Service」を選択
3. 「Connect GitHub」をクリック
4. GitHubアカウントを認証
5. `voice-summary-system` リポジトリを選択
6. 「Connect」をクリック

### 2-2. 設定を入力

#### 基本設定
```
Name: voice-summary-system
Region: Singapore (ap-southeast-1)
Branch: main
Runtime: Python 3
```

#### ビルドコマンド
```
pip install -r requirements.txt
```

#### スタートコマンド
```
python app.py
```

#### 環境変数の設定

「Environment」セクションで以下を追加：

**必須の環境変数：**

```
KEY: OPENAI_API_KEY
VALUE: あなたのOpenAI APIキー
```

```
KEY: GOOGLE_APPLICATION_CREDENTIALS_JSON
VALUE: {"type":"service_account","project_id":"...","private_key":"...","client_email":"..."}
（あなたのservice-account-key.jsonの中身をそのままコピー&ペースト）
```

```
KEY: GCS_BUCKET_NAME
VALUE: voice-summary-audio
```

```
KEY: FLASK_ENV
VALUE: production
```

```
KEY: FLASK_DEBUG
VALUE: False
```

```
KEY: PORT
VALUE: 10000
```

#### 保存してデプロイ

1. 「Create Web Service」をクリック
2. 自動的にデプロイが開始されます（3-5分程度）

---

## 🎉 手順3: デプロイ完了後の確認

### 3-1. デプロイの確認

1. ダッシュボードで「Logs」タブを開く
2. 以下のメッセージが出ていれば成功：
   ```
   Running on http://0.0.0.0:10000
   ```

### 3-2. URLを確認

1. 画面右上のURLを確認（例：`https://voice-summary-system.onrender.com`）
2. このURLをクリックしてアクセス

---

## ⚙️ 手順4: 環境変数の修正（必要に応じて）

### GOOGLE_APPLICATION_CREDENTIALS_JSONの設定

**重要：** `service-account-key.json`の内容を1行にまとめて貼り付ける

1. `configs/service-account-key.json`を開く
2. すべての内容をコピー
3. Renderの環境変数に貼り付け

**例：**
```json
{"type":"service_account","project_id":"your-project","private_key":"-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n","client_email":"your-service-account@your-project.iam.gserviceaccount.com","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/..."}
```

---

## 🐛 トラブルシューティング

### 問題1: デプロイが失敗する

**原因：** 環境変数の設定が不足

**解決方法：**
- 「Environment」タブを確認し、すべての環境変数が正しく設定されているか確認
- 特に`GOOGLE_APPLICATION_CREDENTIALS_JSON`の形式が正しいか確認

### 問題2: アプリにアクセスできない

**原因：** ポート番号の設定ミス

**解決方法：**
- Renderは自動的に`PORT`環境変数を設定します
- `app.py`の`app.run()`が環境変数からポートを読み取っているか確認

### 問題3: APIエラーが発生する

**原因：** APIキーの設定ミス

**解決方法：**
- 環境変数にAPIキーが正しく設定されているか確認
- 「Environment」タブで値を確認（表示は「****」になっているはず）

---

## 💡 Renderの無料プランの制限

- **CPU:** シングルコア
- **メモリ:** 512MB
- **スピン:** 15分間アクセスがないと停止
- **再生:** 次回のアクセス時に自動再起動（約30秒）

**注意：** 
- 15分間アクセスがないとアプリが停止します
- 次回アクセス時に自動再起動（約30秒かかる）

---

## 📝 次のステップ

1. デプロイが完了したら、URLを確認
2. テスト用の音声ファイルをアップロードして動作確認
3. 問題があれば「Logs」タブでエラーログを確認

---

## 🔗 参考リンク

- [Render公式ドキュメント](https://render.com/docs)
- [Flask on Render](https://render.com/docs/deploy-flask)

