import re

with open('gas/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

m = re.search(r'function doLogin\(\)\{.*?\n\}', c, re.DOTALL)
if m:
    with open('dologin_dump.txt', 'w', encoding='utf-8') as out:
        out.write(m.group(0))
    print("Dumped doLogin successfully")

m2 = re.search(r'// APP INIT.*?setTimeout\(dismissSplash', c, re.DOTALL)
if m2:
    with open('boot_dump.txt', 'w', encoding='utf-8') as out:
        out.write(m2.group(0))
    print("Dumped boot section successfully")
