import re

with open('gas/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's inspect the exact JS in gas/index.html around boot and login
scripts = re.findall(r'<script(?:\s+[^>]*)?>(.*?)</script>', html, re.DOTALL)
main_js = [s for s in scripts if len(s) > 1000][0]

# Check for syntax errors like unescaped strings or template literals
print("Checking syntax in main_js...")
# Let's check for backtick and quote balance
lines = main_js.split('\n')
print(f"Total JS lines: {len(lines)}")

# Let's see if there are any obvious issues in bootApp, dismissSplash, doLogin, renderHome
for fn_name in ['bootApp', 'dismissSplash', 'setupInitialView', 'doLogin', 'launchApp', 'renderHome']:
    fn_match = re.search(r'function\s+' + fn_name + r'\s*\([^)]*\)\s*\{', main_js)
    if fn_match:
        print(f"Function {fn_name} found at character {fn_match.start()}")
    else:
        print(f"WARNING: Function {fn_name} NOT found!")
