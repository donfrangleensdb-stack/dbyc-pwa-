import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Extract all IDs in HTML
html_ids = set(re.findall(r'id=["\']([^"\']+)["\']', html))
print(f'Total HTML IDs found: {len(html_ids)}')

# Extract all $('...') calls in JS
js_ids = set(re.findall(r'\$\([\'"]([a-zA-Z0-9_-]+)[\'"]\)', js))
print(f'Total $(\'id\') calls found in JS: {len(js_ids)}')

missing = []
for jid in sorted(js_ids):
    if jid not in html_ids:
        missing.append(jid)

print(f'\nMissing IDs referenced in JS but NOT in HTML ({len(missing)}):')
for m in missing:
    # count occurrences
    count = js.count(f"$('{m}')") + js.count(f'$("{m}")')
    print(f'  - {m} (used {count} times)')
