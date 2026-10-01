with open('gas/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

pos = c.rfind('bootApp')
print("Tail of gas/index.html from bootApp:")
print(c[pos:])
