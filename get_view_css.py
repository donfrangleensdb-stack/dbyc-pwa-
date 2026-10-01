with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re
matches = re.findall(r'\.view\b[^{]*\{[^}]*\}', css)
print("CSS for .view:")
for m in matches:
    print(m)
