with open('gas/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

print('GAS HTML verification:')
print('  File size:', len(c), 'bytes')
print('  Has splash ID:', 'id="splash"' in c)
print('  Has dismissSplash:', 'dismissSplash' in c)
print('  Has auth-screen ID:', 'id="auth-screen"' in c)
print('  Has doLogin:', 'function doLogin' in c)
print('  Has launchApp:', 'function launchApp' in c)
print('  Has safeStorageGet:', 'safeStorageGet' in c)
print('  Has DBYC_LOGO:', 'const DBYC_LOGO' in c)
print('  Has app ID:', 'id="app"' in c)
