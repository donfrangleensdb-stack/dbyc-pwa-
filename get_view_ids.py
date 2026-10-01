with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
all_ids = re.findall(r'id="([^"]+)"', html)
view_ids = [i for i in all_ids if i.startswith('view-') or 'view' in i.lower()]
print(f"All view-related IDs in index.html: {view_ids}")
