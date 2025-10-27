# FFmpeg インストール手順（Windows用）

## 概要
FFmpegは音声・動画ファイルを変換するための無料のツールです。
このシステムでは、ステレオのWAVファイルをモノラルに自動変換するために使用します。

## インストール方法

### 方法1：公式サイトからダウンロード（推奨）

1. **FFmpegのダウンロードページを開く**
   - ブラウザで以下のURLを開く：https://www.gyan.dev/ffmpeg/builds/
   - または、https://ffmpeg.org/download.html からWindows版をダウンロード

2. **FFmpegをダウンロード**
   - 「ffmpeg-release-essentials.zip」をダウンロード
   - ファイルサイズは約100MB程度

3. **ファイルを展開**
   - ダウンロードしたzipファイルを解凍
   - 例：`C:\ffmpeg` に展開

4. **環境変数PATHに追加**
   - Windowsキー + R を押して「ファイル名を指定して実行」を開く
   - `sysdm.cpl` と入力してEnter
   - 「詳細設定」タブを選択
   - 「環境変数」ボタンをクリック
   - 「システム環境変数」の「Path」を選択して「編集」をクリック
   - 「新規」をクリックして、FFmpegのbinフォルダのパスを追加
     - 例：`C:\ffmpeg\bin`
   - 「OK」をクリックしてすべてのダイアログを閉じる

5. **動作確認**
   - PowerShellまたはコマンドプロンプトを開く
   - `ffmpeg -version` と入力してEnter
   - バージョン情報が表示されればインストール成功

### 方法2：Chocolateyを使ったインストール（上級者向け）

既にChocolateyがインストールされている場合は、以下のコマンドでインストールできます：

```powershell
choco install ffmpeg
```

## インストール後の確認

PowerShellまたはコマンドプロンプトで以下のコマンドを実行：

```bash
ffmpeg -version
```

バージョン情報が表示されれば成功です。

## 注意事項

- 環境変数の変更を反映するには、**PowerShellやコマンドプロンプトを再起動**する必要があります
- Flaskサーバーを再起動する必要があります

## トラブルシューティング

### ffmpeg コマンドが見つからない場合
- 環境変数PATHが正しく設定されているか確認
- PowerShellやコマンドプロンプトを再起動しているか確認
- FFmpegが正しくインストールされているか確認
