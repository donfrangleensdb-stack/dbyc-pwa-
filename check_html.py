with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

print('=== INDEX.HTML CHECK ===')
print('bg-slide count:', html.count('bg-slide'))
print('splash ID:', 'id="splash"' in html)
print('auth-screen ID:', 'id="auth-screen"' in html)
print('loginUser ID:', 'id="loginUser"' in html)
print('loginPass ID:', 'id="loginPass"' in html)
print('app ID:', 'id="app"' in html)

print('\n=== SPLASH HTML ===')
s_pos = html.find('id="splash"')
if s_pos != -1:
    print(html[s_pos-20:s_pos+200])

print('\n=== AUTH HTML ===')
a_pos = html.find('id="auth-screen"')
if a_pos != -1:
    print(html[a_pos-20:a_pos+200])
