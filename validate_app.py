import re

with open('gas/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's extract all onclick handlers in the HTML
onclicks = re.findall(r'onclick="([^"]+)"', content)
print(f"Total onclick handlers: {len(onclicks)}")

# Find all functions defined in the script
script_match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
if script_match:
    script_text = script_match.group(1)
    func_defs = set(re.findall(r'function\s+([a-zA-Z0-9_$]+)\s*\(', script_text))
    print(f"Total defined functions in JS: {len(func_defs)}")
    
    # Check if any onclick calls an undefined function
    called_funcs = set()
    for oc in onclicks:
        # extract function calls like doLogin(), goPage('home'), etc.
        calls = re.findall(r'([a-zA-Z0-9_$]+)\s*\(', oc)
        for c in calls:
            called_funcs.add(c)
            
    print(f"Called functions from onclicks: {len(called_funcs)}")
    missing = called_funcs - func_defs
    # Some might be built-ins or standard methods
    builtins = {'closeModal', 'openModal', 'toggleDrawer', 'alert', 'confirm', 'prompt', 'print', 'focus'}
    missing = missing - builtins
    print(f"Potentially missing functions: {missing}")

# Check for all IDs referenced by $('id') or document.getElementById('id')
ids_in_html = set(re.findall(r'id=["\']([^"\']+)["\']', content))
ids_in_js = set(re.findall(r'(?:\$|document\.getElementById)\([\'"]([a-zA-Z0-9_-]+)[\'"]\)', content))

print(f"\nIDs defined in HTML: {len(ids_in_html)}")
print(f"IDs queried in JS: {len(ids_in_js)}")
missing_ids = ids_in_js - ids_in_html
print(f"Missing IDs queried in JS: {missing_ids}")
