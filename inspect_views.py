with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
views = re.findall(r'<div class="[^"]*view[^"]*"[^>]*id="([^"]+)"', html)
print(f"Views in index.html: {views}")

drawer = re.findall(r'<[^>]*class="[^"]*drawer[^"]*"[^>]*id="([^"]+)"', html)
print(f"Drawer elements: {drawer}")

nav_items = re.findall(r'<[^>]*class="[^"]*nav-item[^"]*"[^>]*id="([^"]+)"', html)
print(f"Nav items: {nav_items}")
