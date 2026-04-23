import sys, re
sys.stdout.reconfigure(encoding='utf-8')

# Check if the HTML file itself has encoding issues
with open('vietnamese-words.html', 'rb') as f:
    raw = f.read()

# Check if HTML is UTF-8
try:
    u = raw.decode('utf-8')
    print('HTML file is valid UTF-8')
except Exception as e:
    print('HTML file NOT UTF-8:', e)
    # Try GBK
    try:
        g = raw.decode('gbk')
        print('HTML file IS GBK')
        # Check for Chinese/JS in GBK
        if 'function selVocab' in g:
            print('selVocab found in GBK decode')
    except:
        print('HTML file is neither UTF-8 nor GBK')

# Check for BOM
print('BOM (first 3 bytes):', raw[:3].hex())

# Check key JS strings for encoding issues
with open('vietnamese-words.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Count replacement chars (indicates encoding corruption)
repl = content.count('\ufffd')
print(f'Replacement chars in HTML: {repl}')

# Check if the key strings have proper Chinese
key_strings = ['词库未加载', '预请求', '提示：']
for s in key_strings:
    if s in content:
        print(f'  Chinese OK: {repr(s)}')
    else:
        print(f'  Chinese MISSING: {repr(s)}')

# Check the JavaScript variable declarations
js_strings = ['var VOCAB', 'var VocabLoaded', 'var currentVocab', 'function loadVocabLocal']
for s in js_strings:
    if s in content:
        print(f'  JS OK: {repr(s)}')
    else:
        print(f'  JS MISSING: {repr(s)}')
        
# Check for any obvious garbled Chinese chars (look for common patterns)
garbled = re.findall(r'[\u4e00-\u9fff]{2,}', content)
print(f'\nChinese chars found: {len(garbled)} unique ranges')
# Just print first few to verify they're readable
for g in garbled[:10]:
    print(f'  {repr(g)}')
