with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re
matches = re.findall(r'\.modal[^{]*\{[^}]*\}', css)
print("Modal CSS rules:")
for m in matches[:10]:
    print(m)
