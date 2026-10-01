with open('gas/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

# Extract script text
script_match = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
if script_match:
    script_text = script_match.group(1)
    print(f"JavaScript embedded size: {len(script_text):,} chars")
    
    # Check for core function definitions
    core_checks = [
        'switchView', 'toggleNavigationDrawer', 'navigateFromDrawer',
        'showToast', 'checkAuthSession', 'doMobileLogin', 'doUserLogin',
        'renderMembersRegistry', 'renderTeamsScoreboard', 'renderBirthdays',
        'renderEvents', 'renderMinutes', 'renderNews', 'render15Rules',
        'generateIDCardPreview', 'generateCertificatePreview', 'startQRScanner'
    ]
    
    print("\nCore functions verification:")
    for fn in core_checks:
        defined = f"function {fn}" in script_text
        print(f"  [{'OK' if defined else 'FAIL'}] {fn}")
        
    onclicks = re.findall(r'onclick="([^"]+)"', html)
    all_calls = set()
    for oc in onclicks:
        calls = re.findall(r'([a-zA-Z0-9_$]+)\s*\(', oc)
        for c in calls:
            all_calls.add(c)

    all_defs = set(re.findall(r'function\s+([a-zA-Z0-9_$]+)\s*\(', script_text))
    missing = all_calls - all_defs
    print(f"\nMissing onclick functions in gas/index.html: {sorted(list(missing))}")
