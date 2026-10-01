with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
all_ids = re.findall(r'id=["\']([^"\']+)["\']', html)
views = [i for i in all_ids if 'view' in i.lower() or 'page' in i.lower() or 'section' in i.lower()]
print(f"View-related IDs in index.html: {views}")
