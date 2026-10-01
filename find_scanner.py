with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

import re
matches = [m.start() for m in re.finditer(r'scanner|Scanner', c)]
print(f"Found {len(matches)} occurrences of scanner")

# Find function definitions related to scanner
fn_matches = re.findall(r'function\s+([a-zA-Z0-9_$]*[sS]canner[a-zA-Z0-9_$]*)\s*\(', c)
print(f"Scanner-related functions: {fn_matches}")

pos = c.find('stopScanner')
if pos != -1:
    print("Around stopScanner:")
    print(c[pos-200:pos+500])
