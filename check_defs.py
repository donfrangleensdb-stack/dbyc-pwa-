with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

print("Is switchView defined as a function in app.js?", "function switchView" in js)
print("Is toggleNavigationDrawer defined as a function in app.js?", "function toggleNavigationDrawer" in js)
print("Is goPage defined as a function in app.js?", "function goPage" in js)
print("Is toggleDrawer defined as a function in app.js?", "function toggleDrawer" in js)
