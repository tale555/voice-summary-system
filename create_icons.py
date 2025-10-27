"""
PWA用アイコン生成スクリプト
簡単なアイコンを作成します
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
except ImportError:
    print("Pillow がインストールされていません")
    print("インストール: pip install Pillow")
    exit(1)


def create_icon(size, filename):
    """アイコンを作成"""
    # 画像を作成
    img = Image.new('RGB', (size, size), color='#667eea')
    draw = ImageDraw.Draw(img)
    
    # 中央に円を描画
    margin = size // 8
    draw.ellipse(
        [margin, margin, size - margin, size - margin],
        fill='#764ba2',
        outline='white',
        width=size // 32
    )
    
    # マイクのアイコン（簡単な図形）
    mic_width = size // 3
    mic_height = size // 2
    mic_x = (size - mic_width) // 2
    mic_y = (size - mic_height) // 2
    
    # マイクのボディ
    draw.rectangle(
        [mic_x + mic_width // 4, mic_y, mic_x + 3 * mic_width // 4, mic_y + 3 * mic_height // 4],
        fill='white'
    )
    
    # マイクのスタンド
    draw.rectangle(
        [mic_x + mic_width // 2 - mic_width // 8, mic_y + 3 * mic_height // 4, 
         mic_x + mic_width // 2 + mic_width // 8, mic_y + mic_height],
        fill='white'
    )
    
    # ベース
    draw.ellipse(
        [mic_x, mic_y + 7 * mic_height // 8, mic_x + mic_width, mic_y + mic_height],
        fill='white'
    )
    
    # 保存
    img.save(filename)
    print(f"✓ アイコンを作成しました: {filename}")


def main():
    """メイン処理"""
    # staticディレクトリを確認
    static_dir = 'static'
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
        print(f"✓ {static_dir} ディレクトリを作成しました")
    
    # アイコンを作成
    create_icon(192, os.path.join(static_dir, 'icon-192.png'))
    create_icon(512, os.path.join(static_dir, 'icon-512.png'))
    
    print("\n✓ すべてのアイコンを作成しました！")


if __name__ == '__main__':
    main()
