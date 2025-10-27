# デプロイ準備ガイド

音声要約システムを本番環境で運用するためのガイドです。

## 📋 目次

1. [デプロイ方法の選択](#デプロイ方法の選択)
2. [セキュリティ設定](#セキュリティ設定)
3. [本番用設定](#本番用設定)
4. [運用監視](#運用監視)
5. [トラブルシューティング](#トラブルシューティング)

---

## デプロイ方法の選択

### 1. ローカルPC運用（現在の方式）

**特徴：**
- 開発環境をそのまま使用
- 同一ネットワーク内からアクセス可能
- 追加費用なし

**手順：**
```powershell
# voice_summary_systemディレクトリで実行
python app.py
```

**アクセス：**
- 同じPC: `http://127.0.0.1:5000`
- 同じネットワーク: `http://192.168.11.2:5000`（PCのIP）

### 2. クラウドデプロイ（推奨）

#### A. Google Cloud Platform (GCP)

**特徴：**
- Google Cloud Speech-to-Textとの統合が容易
- スケーラブル
- 長時間運用可能

**推奨サービス：**
- **Cloud Run**: サーバーレス、自動スケール
- **Compute Engine**: 固定サーバー

#### B. Heroku

**特徴：**
- 簡単なデプロイ
- 無料プランあり
- ドキュメント充実

#### C. Railway / Render

**特徴：**
- 初心者向け
- 簡単なセットアップ
- 無料プランあり

---

## セキュリティ設定

### 1. APIキーの保護

#### 現在の設定（開発環境）
```env
OPENAI_API_KEY=your-api-key-here
```

#### 推奨設定（本番環境）

**方法1: 環境変数の使用**
```bash
# Windows (PowerShell)
$env:OPENAI_API_KEY = "your-api-key-here"

# Linux/Mac
export OPENAI_API_KEY="your-api-key-here"
```

**方法2: クラウドのシークレット管理**
- GCP: Secret Manager
- AWS: Secrets Manager
- Azure: Key Vault

### 2. HTTPS（SSL/TLS）の設定

**必須項目：**
- 本番環境では必ずHTTPSを使用
- 証明書の取得（Let's Encrypt、Cloudflare等）

**FlaskでHTTPS対応：**
```python
# app.py の最後の部分を変更
if __name__ == '__main__':
    # 開発環境
    if app.config['FLASK_ENV'] == 'development':
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        # 本番環境（HTTPS対応）
        app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')
```

### 3. ファイルアップロードの制限

現在の設定：
```python
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
```

**推奨設定：**
- 一般ユーザー: 50MB
- 管理者: 100MB

---

## 本番用設定

### 1. 設定ファイルの変更

`config.py` を本番用に調整：

```python
# 本番環境の判定
import os
PRODUCTION = os.getenv('PRODUCTION', 'False').lower() == 'true'

if PRODUCTION:
    # 本番環境設定
    FLASK_DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')  # 環境変数から取得
else:
    # 開発環境設定
    FLASK_DEBUG = True
    SECRET_KEY = 'your-secret-key-here'
```

### 2. ログの設定

本番環境では詳細なログを記録：

```python
import logging

# ログレベルの設定
if PRODUCTION:
    logging.basicConfig(
        level=logging.INFO,
        filename='app.log',
        format='%(asctime)s %(levelname)s %(message)s'
    )
```

### 3. エラーハンドリングの強化

```python
@app.errorhandler(500)
def internal_error(error):
    """サーバーエラー時の処理"""
    logger.error(f"Internal Error: {error}")
    return jsonify({'error': 'サーバーエラーが発生しました'}), 500

@app.errorhandler(404)
def not_found(error):
    """404エラー時の処理"""
    return jsonify({'error': 'ページが見つかりません'}), 404
```

---

## 運用監視

### 1. ログの確認

```bash
# Flaskサーバーのログ
tail -f app.log

# Windows PowerShell
Get-Content app.log -Wait -Tail 50
```

### 2. パフォーマンス監視

**推奨ツール：**
- **Flask-MonitoringDashboard**: Flaskアプリの監視
- **Prometheus**: メトリクス収集
- **Grafana**: 可視化

### 3. API使用量の監視

**Google Cloud Speech-to-Text:**
- GCP Console → Speech-to-Text → 使用量

**OpenAI API:**
- OpenAI Platform → Usage

---

## トラブルシューティング

### 1. サーバーが起動しない

**原因:**
- ポート5000が既に使用されている
- 必要なライブラリが不足

**解決方法:**
```powershell
# ポートを変更（例: 8000）
python app.py
# または app.py の最後の行を変更
app.run(host='0.0.0.0', port=8000)
```

### 2. 外部からアクセスできない

**原因:**
- ファイアウォールの設定
- ルーターの設定

**解決方法:**
- Windowsファイアウォールでポート5000を開く
- ルーターでポート転送を設定

### 3. メモリ不足エラー

**原因:**
- 大きな音声ファイルの処理
- メモリリーク

**解決方法:**
- ファイルサイズの制限を強化
- 処理後にメモリをクリア

---

## 次のステップ

### 推奨事項

1. **テスト環境の構築**
   - 本番前にテスト環境で動作確認

2. **バックアップの設定**
   - 重要なデータの定期バックアップ

3. **セキュリティ監査**
   - 定期的なセキュリティチェック

4. **ドキュメント整備**
   - 運用マニュアルの作成

### 問い合わせ先

- システム管理者
- 開発者

---

## 参考資料

- [Flask公式ドキュメント](https://flask.palletsprojects.com/)
- [Google Cloud Speech-to-Text](https://cloud.google.com/speech-to-text)
- [OpenAI API](https://platform.openai.com/docs)
