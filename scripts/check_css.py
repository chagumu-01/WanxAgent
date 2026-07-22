import glob

files = glob.glob('d:/OmniAgent/src/frontend/dist/assets/index-*.css')
for f in files:
    content = open(f, encoding='utf-8').read()
    count = content.count('c41e3a')
    print(f'文件 {f}: c41e3a出现次数={count}')
    
    if 'c41e3a' in content:
        idx = content.index('c41e3a')
        print(f'  上下文: {content[idx-50:idx+50]}')
    
    if ':root' in content:
        idx = content.index(':root')
        print(f'  :root上下文: {content[idx:idx+300]}')