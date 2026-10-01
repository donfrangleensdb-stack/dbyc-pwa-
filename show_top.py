with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

lines = js.split('\n')
for i in range(min(150, len(lines))):
    print(f"{i+1}: {lines[i]}")
