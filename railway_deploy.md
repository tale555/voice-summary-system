# Railwayクラウドデプロイガイド

音声要約システムをRailwayでデプロイする方法です。

## 🚀 Railwayとは？

- **簡単**: GitHubと連携するだけで自動デプロイ
- **無料プランあり**: 月$5のクレジットが毎月無料で提供
- **高速**: 数分でデプロイ完了
- **自動SSL**: HTTPSが自動設定される

## 📋 必要なもの

1. GitHubアカウント（無料）
2. Railwayアカウント（無料）
3. 現在のコード

## 🎯 デプロイ手順

### ステップ1: GitHubにコードをアップロード

#### 1-1. GitHubでリポジトリを作成

1. https://github.com にアクセス
2. 右上の「+」→「New repository」をクリック
3. 以下を入力：
   - Repository name: `voice-summary-system`
   - Description: 音声要約システム
   - Public を選択
4. 「Create repository」をクリック

#### 1-2. ローカルからGitHubにプッシュ

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

# 5. GitHubリポジトリを追加（URLは作成したリポジトリのURLに変更）
git remote add origin https://github.com/あなたのユーザー名/voice-summary-system.git

# 6. プッシュ
git push -u origin main
```

**GitHub認証が必要な場合：**
- Personal Access Tokenを生成
- トークンをパスワードとして使用

### ステップ2: Railwayでデプロイ

#### 2-1. Railwayに登録

1. https://railway.app にアクセス
2. 「Login」→「Github」を選択
3. GitHub認証を許可
4. 「New Project」をクリック

#### 2-2. プロジェクトを作成

1. 「Deploy from Github repo」を選択
2. 作成したリポジトリを選択
3. 「Deploy」をクリック
4. 数分待つと自動でデプロイ開始

### ステップ3: 環境変数の設定

デプロイ後、Railwayの画面で以下を設定：

#### 3-1. サービスアカウントキーの設定

1. Railwayのプロジェクト → Settings → Variables
2. 以下を追加：

```
GOOGLE_APPLICATION_CREDENTIALS_JSON = {ここにservice-account-key.jsonの内容を貼り付け}
```

**注意**: JSONファイルの内容をそのまま貼り付け

#### 3-2. その他の環境変数

```
OPENAI_API_KEY = あなたのOpenAI API キー
GCS_BUCKET_NAME = voice-summary-audio
```

### ステップ4: サービスアカウントキーのアップロード

Railwayではローカルファイルを直接使えないため、環境変数として設定：

1. `configs/service-account-key.json`を開く
2. ファイルの内容を全てコピー
3. Railwayの環境変数として設定

#### コードを修正（Railway対応）

`config.py`を修正して環境変数から読み込めるようにする必要があります。

## 🔧 Railway用の修正

### 必要なコード修正

1. `config.py`を修正して環境変数JSON対応を追加
2. `app.py`でポート番号を自動取得
3. `.gitignore`を作成（秘密情報を除外）

## 📝 注意事項

### クレジット使用量

- 無料プラン: 月$5のクレジット
- 使用量が$5を超えると課金
- 開発環境なら無料で運用可能

### 再デプロイ

GitHubにプッシュすると自動的に再デプロイされます。

## 🔗 デプロイ後のアクセス

デプロイ完了後、Railwayが自動でURLを生成：

```
https://あなたのプロジェクト名.up.railway.app
```

このURLからどこでもアクセス可能です！

## ❓ トラブルシューティング

### デプロイが失敗する

- 環境変数の設定を確認
- ログを確認してエラーをチェック

### アクセスできない

- デプロイの完了を確認
- URLが正しいか確認

## 📞 サポート

問題がある場合は、Railwayのドキュメントを参照：
https://docs.railway.app
