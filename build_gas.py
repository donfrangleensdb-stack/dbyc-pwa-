import base64, os

# Read source files
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

css_path = 'css/style.css' if os.path.exists('css/style.css') else 'styles.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

js_path = 'js/app.js' if os.path.exists('js/app.js') else 'app.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Inline CSS
html = html.replace('<link rel="stylesheet" href="css/style.css">', '<style>\n' + css + '\n</style>')
html = html.replace('<link rel="stylesheet" href="styles.css"/>', '<style>\n' + css + '\n</style>')

# Remove manifest
html = html.replace('<link rel="manifest" href="manifest.json">', '<!-- PWA manifest: not used in GAS iframe -->')
html = html.replace('<link rel="manifest" href="manifest.json"/>', '<!-- PWA manifest: not used in GAS iframe -->')

# Inline JS
html = html.replace('<script src="js/app.js"></script>', '<script>\n' + js + '\n</script>')
html = html.replace('<script src="app.js"></script>', '<script>\n' + js + '\n</script>')

# Ensure gas directory exists
os.makedirs('gas', exist_ok=True)
out_path = os.path.join('gas', 'index.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)

sz = os.path.getsize(out_path)
print(f'\nGoogle Apps Script index.html ready!')
print(f'  Path: gas/index.html')
print(f'  Size: {sz:,} bytes ({sz/1024:.1f} KB)')
print(f'  Status: {"PERFECT (under 500KB GAS limit)" if sz < 500000 else "EXCEEDS LIMIT"}')
