with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
modals = re.findall(r'<div\s+[^>]*class="[^"]*modal[^"]*"[^>]*id="([^"]+)"', html)
print(f"Modals in index.html: {modals}")

all_modal_ids = [m for m in re.findall(r'id="([^"]+)"', html) if 'modal' in m.lower()]
print(f"All modal-like IDs: {all_modal_ids}")
