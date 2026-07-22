import glob

files = glob.glob('d:/OmniAgent/src/frontend/dist/assets/index-*.css')
for f in files:
    content = open(f, encoding='utf-8').read()
    count = content.count('newsprint')
    print(f'文件 {f}: newsprint出现次数={count}')
    
    count2 = content.count('--el-color-primary')
    print(f'文件 {f}: --el-color-primary出现次数={count2}')
    
    if '--el-color-primary' in content:
        idx = content.index('--el-color-primary')
        print(f'  上下文: {content[idx:idx+150]}')