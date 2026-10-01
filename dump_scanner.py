with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

import re
m = re.search(r'function startScanner.*?function stopScanner', c, re.DOTALL)
if m:
    with open('scanner_dump.txt', 'w', encoding='utf-8') as out:
        out.write(m.group(0))
    print("Dumped scanner functions")
else:
    print("Scanner functions not found in that range")
