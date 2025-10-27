# Railwayデプロイ - 実際の手順

このファイルでは、実際にRailwayにデプロイするための具体的な手順を説明します。

## 📋 前提条件

- ✅ コードの準備が完了している
- ✅ GitHubアカウントを持っている
- ✅ Google Cloud Speech-to-Text APIの設定が完了している
- ✅ OpenAI API キーを取得している

## 🎯 手順1: GitHubにコードをアップロード

### 1-1. GitHubでリポジトリを作成

1. ブラウザで https://github.com を開く
2. 右上の「+」ボタンをクリック
3. 「New repository」をクリック
4. 以下を入力：
   - **Repository name**: `voice-summary-system`（任意の名前でOK）
   - **Description**: `音声要約システム`
   - **Public** を選択（無料で使うため）
5. 下にスクロールして「Create repository」をクリック

### 1-2. Gitをインストール（まだの場合）

Gitがインストールされていない場合：
1. https://git-scm.com/download/win を開く
2. ダウンロードしたファイルを実行
3. デフォルト設定でインストール
4. PowerShellを再起動

### 1-3. ローカルからGitHubにコードをアップロード

PowerShellで以下を実行：

```powershell
# 1. voice_summary_systemディレクトリに移動
cd "C:\Users\mhero\OneDrive\デスクトップ\cursor練習\voice_summary_system"

# 2. Gitリポジトリを初期化
git init

# 3. ファイルを追加
git add .

# 4. コミット
git commit -m "初回コミット"

# 5. ブランチをmainに変更（GitHubのデフォルト）
git branch -M main

# 6. GitHubリポジトリを追加
# 注: YOUR_USERNAME を自分のGitHubユーザー名に変更
git remote add origin https://github.com/YOUR_USERNAME/voice-summary-system.git

# 7. プッシュ
git push -u origin main
```

**認証について:**
- ユーザー名: 自分のGitHubユーザー名
- パスワード: Personal Access Token（後述）

### 1-4. GitHub Personal Access Tokenの作成

1. GitHubにログイン
2. 右上のプロフィール画像 → 「Settings」
3. 左メニューの一番下「Developer settings」
4. 「Personal access tokens」→「Tokens (classic)」
5. 「Generate new token」→「Generate new token (classic)」
6. 以下を入力：
   - Note: `Railway Deploy`
   - Expiration: `90 days`（お好みで）
   - Scopes: `repo` にチェック（全て自動でチェックされる）
7. 「Generate token」をクリック
8. **トークンをコピー**（後で見れないので必ずコピー！）
9. このトークンをGitのパスワードとして使用

## 🎯 手順2: Railwayでデプロイ

### 2-1. Railwayに登録

1. https://railway.app を開く
2. 「Login」をクリック
3. 「Github」を選択
4. GitHub認証を許可

### 2-2. プロジェクトを作成

1. 「+ New Project」をクリック
2. 「Deploy from Github repo」を選択
3. 作成したリポジトリ `voice-summary-system` を選択
4. Railwayが自動でコードを取得してデプロイを開始

### 2-3. 環境変数を設定

1. Railwayのプロジェクト画面で「Variables」タブをクリック
2. 「+ New Variable」をクリックして以下を追加：

#### 必須の環境変数

```
名前: OPENAI_API_KEY
値: あなたのOpenAI APIキー（環境変数から取得）
```

```
名前: GCS_BUCKET_NAME
値: voice-summary-audio
```

#### サービスアカウントキーの設定

1. 自分のPCで以下を開く：
   ```
   voice_summary_system\configs\service-account-key.json
   ```

2. ファイルの中身を全てコピー（Ctrl+A → Ctrl+C）

3. Railwayで新しい環境変数を追加：
   ```
   名前: GOOGLE_APPLICATION_CREDENTIALS_JSON
   値: [コピーしたJSONの内容を貼り付け]
   ```

**注意**: 値に余計な文字やスペースが入らないように注意！

### 2-4. デプロイ完了を待つ

1. Railwayの「Deployments」タブでデプロイ状況を確認
2. 緑色のチェックマークが表示されれば完了
3. URLが自動生成される（例: `https://voice-summary-system.up.railway.app`）

## ✅ 完了！

これでクラウド上でシステムが稼働しています。

### アクセス方法

1. Railwayの「Settings」→「Networking」で確認できるURL
2. このURLをブラウザで開く
3. どこからでもアクセス可能！

## 🔄 更新方法

コードを変更してGitHubにプッシュすると、Railwayが自動で再デプロイします：

```powershell
cd "C:\Users\mhero\OneDrive\デスクトップ\cursor練習\voice_summary_system"
git add .
git commit -m "更新内容"
git push origin main
```

## 📞 トラブルシューティング

### デプロイが失敗する

1. Railwayの「Deployments」→「View Logs」でエラーを確認
2. 環境変数の設定を再確認
3. JSONファイルの形式が正しいか確認

### アクセスできない

1. デプロイが完了しているか確認（緑のチェックマーク）
2. URLをコピー＆ペーストして正しく入力
3. 数分待ってから再試行

## 💡 ヒント

- 無料プランは月$5のクレジットが提供されます
- 使用量は Railway のダッシュボードで確認できます
- 使用量が$5を超えると一時的に停止する可能性があります

