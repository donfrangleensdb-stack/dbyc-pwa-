with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
all_funcs = re.findall(r'function\s+([a-zA-Z0-9_$]+)\s*\(', js)
print(f"Total functions currently in app.js: {len(all_funcs)}")
for fn in sorted(all_funcs):
    print(f"  - {fn}")
