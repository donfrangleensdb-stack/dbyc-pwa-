with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re
matches = re.findall(r'.{0,30}(?:view|drawer|active).{0,30}', css)
print("CSS references to view / drawer:")
for m in matches[:20]:
    print(m.strip())
