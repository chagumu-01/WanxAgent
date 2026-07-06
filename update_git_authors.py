import subprocess

OLD_TO_NEW = {
    ("组长", "group_leader@example.com"): ("梁思宇", "liangsiyu-1687824443@qq.com"),
    ("组员A", "member_a@example.com"): ("倪丹", "nidan-3386314071@qq.com"),
    ("组员B", "member_b@example.com"): ("夏丽莎", "xialisha-1628790282@qq.com"),
    ("初始化", "init@example.com"): ("梁思宇", "liangsiyu-1687824443@qq.com"),
}


def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, cwd="d:/OmniAgent", capture_output=True, text=True)
    if result.returncode != 0:
        print(f"命令失败: {cmd}")
        print(f"错误: {result.stderr[:200]}")
    return result


def main():
    print("=" * 60)
    print("更新Git提交作者信息")
    print("=" * 60)
    
    print("\n修改映射:")
    for (old_name, old_email), (new_name, new_email) in OLD_TO_NEW.items():
        print(f"  {old_name} <{old_email}> -> {new_name} <{new_email}>")
    
    print("\n" + "=" * 60)
    print("步骤1: 使用git filter-branch修改历史提交")
    print("=" * 60)
    
    for (old_name, old_email), (new_name, new_email) in OLD_TO_NEW.items():
        print(f"\n修改 {old_name} 的提交...")
        
        cmd = f"""git filter-branch --env-filter '
        OLD_EMAIL="{old_email}"
        NEW_NAME="{new_name}"
        NEW_EMAIL="{new_email}"
        
        if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]; then
            export GIT_COMMITTER_NAME="$NEW_NAME"
            export GIT_COMMITTER_EMAIL="$NEW_EMAIL"
        fi
        if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]; then
            export GIT_AUTHOR_NAME="$NEW_NAME"
            export GIT_AUTHOR_EMAIL="$NEW_EMAIL"
        fi
        ' HEAD"""
        
        result = run_cmd(cmd)
        if result.returncode == 0:
            print(f"  ✓ 成功修改 {old_name} 的提交")
        else:
            print(f"  ✗ 修改失败")
    
    print("\n" + "=" * 60)
    print("步骤2: 验证修改结果")
    print("=" * 60)
    
    print("\n提交历史:")
    result = run_cmd('git log --format="%h - %an (%ae): %s" --reverse')
    print(result.stdout)
    
    print("\n贡献统计:")
    result = run_cmd("git log --format='%an' | Sort-Object -Unique | ForEach-Object { $name = $_; $count = (git log --format='%an' | Where-Object { $_ -eq $name }).Count; Write-Output \"$count - $name\" }")
    print(result.stdout)


if __name__ == "__main__":
    main()