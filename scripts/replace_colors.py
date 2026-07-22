import os

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "src", "frontend", "src")

COLOR_MAP = {
    "#c41e3a": "#111111",
    "#d94560": "#404040",
    "#e87187": "#737373",
    "#f2a5b5": "#A3A3A3",
    "#f8d0d8": "#E5E5E0",
    "#fceef2": "#F9F9F7",
    "#4a1a25": "#111111",
}

def replace_colors_in_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        original_content = content
        for old_color, new_color in COLOR_MAP.items():
            content = content.replace(old_color, new_color)
        
        if content != original_content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ 已更新: {filepath}")
            return True
        return False
    except Exception as e:
        print(f"❌ 处理失败: {filepath} - {e}")
        return False

def main():
    updated_count = 0
    total_files = 0
    
    for root, dirs, files in os.walk(BASE_DIR):
        for filename in files:
            if filename.endswith((".vue", ".scss", ".css")):
                filepath = os.path.join(root, filename)
                total_files += 1
                if replace_colors_in_file(filepath):
                    updated_count += 1
    
    print(f"\n🎉 完成! 共扫描 {total_files} 个文件，更新了 {updated_count} 个文件")

if __name__ == "__main__":
    main()