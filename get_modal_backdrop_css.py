with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re
matches = re.findall(r'(\.modal-backdrop|\.modal-overlay|\.modal)[^{]*\{[^}]*\}', css)
print("Modal display rules:")
for m in matches:
    print(m)
