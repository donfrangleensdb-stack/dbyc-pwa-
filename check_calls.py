with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

import re
all_calls = set(re.findall(r'([a-zA-Z0-9_$]+)\s*\(', c))
all_defs = set(re.findall(r'function\s+([a-zA-Z0-9_$]+)\s*\(', c))

standard_js = {
    'if', 'for', 'while', 'switch', 'catch', 'function', 'return',
    'require', 'import', 'export', 'parseInt', 'parseFloat', 'isNaN', 'isFinite',
    'encodeURIComponent', 'decodeURIComponent', 'encodeURI', 'decodeURI',
    'alert', 'confirm', 'prompt', 'setTimeout', 'setInterval', 'clearTimeout', 'clearInterval',
    'fetch', 'btoa', 'atob', 'addEventListener', 'removeEventListener', 'dispatchEvent',
    'querySelector', 'querySelectorAll', 'getElementById', 'getElementsByClassName',
    'getElementsByTagName', 'createElement', 'appendChild', 'removeChild', 'replaceChild',
    'setAttribute', 'getAttribute', 'removeAttribute', 'classList', 'add', 'remove', 'toggle',
    'contains', 'indexOf', 'lastIndexOf', 'includes', 'startsWith', 'endsWith', 'slice',
    'substring', 'substr', 'split', 'join', 'replace', 'replaceAll', 'match', 'matchAll',
    'search', 'toLowerCase', 'toUpperCase', 'trim', 'trimStart', 'trimEnd', 'padStart',
    'padEnd', 'charAt', 'charCodeAt', 'codePointAt', 'concat', 'push', 'pop', 'shift',
    'unshift', 'splice', 'sort', 'reverse', 'map', 'filter', 'reduce', 'reduceRight',
    'forEach', 'some', 'every', 'find', 'findIndex', 'findLast', 'findLastIndex', 'flat',
    'flatMap', 'fill', 'copyWithin', 'entries', 'keys', 'values', 'toString', 'valueOf',
    'toLocaleString', 'hasOwnProperty', 'isPrototypeOf', 'propertyIsEnumerable',
    'assign', 'create', 'defineProperty', 'defineProperties', 'freeze', 'seal',
    'preventExtensions', 'isExtensible', 'isFrozen', 'isSealed', 'getOwnPropertyDescriptor',
    'getOwnPropertyDescriptors', 'getOwnPropertyNames', 'getOwnPropertySymbols', 'getPrototypeOf',
    'setPrototypeOf', 'fromEntries', 'all', 'race', 'allSettled', 'any', 'resolve', 'reject',
    'then', 'catch', 'finally', 'then', 'json', 'text', 'blob', 'arrayBuffer', 'formData',
    'getItem', 'setItem', 'removeItem', 'clear', 'key', 'now', 'parse', 'stringify',
    'min', 'max', 'abs', 'round', 'floor', 'ceil', 'random', 'sqrt', 'pow', 'log', 'exp',
    'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'atan2', 'open', 'close', 'print', 'focus',
    'blur', 'scroll', 'scrollTo', 'scrollBy', 'write', 'writeln', 'postMessage', 'requestAnimationFrame',
    'cancelAnimationFrame', 'createObjectURL', 'revokeObjectURL', 'readAsDataURL', 'readAsText',
    'readAsArrayBuffer', 'readAsBinaryString', 'send', 'setRequestHeader', 'abort',
    'getContext', 'drawImage', 'toDataURL', 'toBlob', 'save', 'restore', 'beginPath',
    'closePath', 'moveTo', 'lineTo', 'stroke', 'fill', 'rect', 'arc', 'fillText', 'strokeText',
    'measureText', 'setFontSize', 'setTextColor', 'text', 'addPage', 'splitTextToSize',
    'QRCode', 'jsPDF', 'html2canvas', 'FileReader', 'Blob', 'Date', 'Array', 'Object',
    'String', 'Number', 'Boolean', 'RegExp', 'Error', 'TypeError', 'RangeError', 'SyntaxError',
    'ReferenceError', 'URIError', 'EvalError', 'Promise', 'URL', 'Math', 'JSON', 'console',
    'log', 'warn', 'error', 'info', 'debug', 'table', 'trace', 'group', 'groupEnd',
    'groupCollapsed', 'time', 'timeEnd', 'timeLog', 'count', 'countReset', 'clear',
    'assert', 'dir', 'dirxml', 'res', 'rej', 'm', 'd', 'u', 'a', 'b', 'e', 'x', 'y', 'z', 'i',
    'f', 't', 'p', 'l', 'w', 'h', 'c', 'g', 'v', 'k', 's', 'r', 'q', 'n', 'o'
}

called_not_defined = all_calls - all_defs - standard_js
print("Called functions that are NOT defined in app.js:")
for cnd in sorted(called_not_defined):
    print(f"  - {cnd}")
