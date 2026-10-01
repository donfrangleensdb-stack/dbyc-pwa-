with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
onclicks = re.findall(r'onclick="([^"]+)"', html)
all_calls = set()
for oc in onclicks:
    calls = re.findall(r'([a-zA-Z0-9_$]+)\s*\(', oc)
    for c in calls:
        all_calls.add(c)

all_defs = set(re.findall(r'function\s+([a-zA-Z0-9_$]+)\s*\(', js))

missing = all_calls - all_defs
print(f"Total onclick function calls: {len(all_calls)}")
print(f"Missing functions in app.js: {sorted(list(missing))}")
