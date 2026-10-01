with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

check_list = ['showToast', 'switchView', 'openAwardPointsModal', 'toggleNavigationDrawer', 'stopScanner', 'initSalesianTheme', 'showInstallButtons']

print("Checking suspicious function names:")
for name in check_list:
    in_js = name in js
    in_html = name in html
    print(f"  {name}: in app.js={in_js}, in index.html={in_html}")
