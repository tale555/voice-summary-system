# 環境変数を更新
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# FFmpegの確認
Write-Host "FFmpeg の確認中..." -ForegroundColor Yellow
ffmpeg -version

# プロジェクトディレクトリに移動
cd "C:\Users\mhero\OneDrive\デスクトップ\cursor練習\voice_summary_system"

# Flaskサーバーを起動
Write-Host "`nFlaskサーバーを起動中..." -ForegroundColor Green
python app.py
