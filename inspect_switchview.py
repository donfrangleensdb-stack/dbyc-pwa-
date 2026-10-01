with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
matches = [m.start() for m in re.finditer(r'switchView', js)]
print(f"Occurrences of switchView in app.js: {len(matches)}")
for idx, pos in enumerate(matches):
    print(f"Match {idx+1}:")
    print(js[max(0, pos-100):min(len(js), pos+300)])
    print("-" * 50)
