import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

html_ids = set(re.findall(r'id=["\']([^"\']+)["\']', html))

# Find all document.getElementById('xxx').something (without optional chaining ?.)
matches = re.findall(r'document\.getElementById\(["\']([^"\']+)["\']\)\.([a-zA-Z0-9_$]+)', js)
unsafe = []
for el_id, prop in matches:
    if el_id not in html_ids and el_id not in ['qrVideo', 'printCertificateFrame', 'certPhotoPreview', 'memberPassPhotoPreview']:
        unsafe.append((el_id, prop))

print(f"Total unsafe DOM queries without null check: {len(unsafe)}")
for u in set(unsafe):
    print(f"  Unsafe: document.getElementById('{u[0]}').{u[1]}")
