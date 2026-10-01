with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
all_ids = re.findall(r'id=["\']([^"\']+)["\']', html)
print(f"Total IDs in index.html: {len(all_ids)}")
print("First 40 IDs in index.html:")
for i in all_ids[:40]:
    print(f"  - {i}")
