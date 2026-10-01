with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
matches = re.findall(r'<div\s+[^>]*id="view-[^"]*"[^>]*>', html)
print("View elements in index.html:")
for m in matches:
    print(m)
