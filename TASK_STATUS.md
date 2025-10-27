# タスクステータス

## 現在の状態：音声認識でエラー発生中

### 問題点
- Google Cloud Speech-to-Text APIが**ステレオ（2チャンネル）のWAVファイルを受け付けない**
- エラーメッセージ：「Must use single channel (mono) audio, but WAV header indicates 2 channels.」
- `pydub`による音声変換機能は実装済みだが、FFmpegがインストールされていないため動作しない

### 実装済み機能
- ✅ プロジェクトフォルダ構成
- ✅ Google Cloud Speech-to-Text API連携
- ✅ OpenAI API連携（要約機能）
- ✅ Flask Webサーバー
- ✅ ファイルアップロード機能
- ✅ 音声変換機能のコード実装（動作せず）
- ✅ Webインターフェース
- ❌ ステレオ→モノラル自動変換機能（動作せず）

### ユーザーへの要求
現在のところ、**モノラル形式で録音されたWAVファイルを使用する必要があります。**

### 今後の改善案
1. FFmpegをインストールして音声変換機能を有効化
2. 代替の音声変換ライブラリの使用
3. 録音時の形式チェック機能の追加
