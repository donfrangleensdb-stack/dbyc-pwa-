import os

print("Synchronizing Google Apps Script files...")

# 1. Read style.css -> style.html
with open("style.css", "r", encoding="utf-8") as f:
    css_content = f.read()

with open("style.html", "w", encoding="utf-8") as f:
    f.write("<style>\n" + css_content + "\n</style>")

# 2. Read app.js -> javascript.html
with open("app.js", "r", encoding="utf-8") as f:
    js_content = f.read()

with open("javascript.html", "w", encoding="utf-8") as f:
    f.write("<script>\n" + js_content + "\n</script>")

# 3. Read index.html -> gas_index.html
with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Replace <link rel="stylesheet" href="style.css" /> with <?!= include('style'); ?>
# Replace <script src="app.js"></script> with <?!= include('javascript'); ?>
gas_html = html_content.replace(
    '<link rel="stylesheet" href="style.css" />',
    "<?!= include('style'); ?>"
)
gas_html = gas_html.replace(
    '<script src="app.js"></script>',
    "<?!= include('javascript'); ?>"
)

with open("gas_index.html", "w", encoding="utf-8") as f:
    f.write(gas_html)

print("GAS files synchronized successfully!")
