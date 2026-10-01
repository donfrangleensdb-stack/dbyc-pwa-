with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
matches = re.findall(r'.{0,50}(?:switchView|toggleNavigationDrawer|showToast|openAwardPointsModal).{0,50}', html)
for m in matches:
    print(m.strip())
