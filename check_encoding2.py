import sys
sys.stdout.reconfigure(encoding='utf-8')

# Read the raw bytes of vocab.js and check for encoding mix
with open('vietnamese-vocab.js', 'rb') as f:
    raw = f.read()

# The starter array should be around bytes 100-30000
# Find 'như' in bytes
nhu_utf8 = 'như'.encode('utf-8')
nhu_idx = raw.find(nhu_utf8)
print(f"'như' (UTF-8) found at byte offset: {nhu_idx}")

# Find the Chinese chars after như - in the JSON they should be '作为'
# Try both UTF-8 and GBK
zuowei_utf8 = '作为'.encode('utf-8')
zuowei_gbk = '作为'.encode('gbk')

idx_after_nhu = nhu_idx + len(nhu_utf8)
print(f"Bytes after như: {raw[idx_after_nhu:idx_after_nhu+30].hex()}")
print(f"  Looking for UTF-8 '作为': {zuowei_utf8.hex()} -> found at {raw.find(zuowei_utf8)}")
print(f"  Looking for GBK '作为': {zuowei_gbk.hex()} -> found at {raw.find(zuowei_gbk)}")

# Check the raw bytes around như position
# UTF-8 of '作为' = e4 bd 5c e4 wc bd (wrong!)
# GBK of '作为' = d7 aa ce c3 (wrong!)  
# Wait let me recalculate
print()
print("=== Checking Chinese encoding ===")
print(f"UTF-8 '作为': {'作为'.encode('utf-8').hex()}")
print(f"GBK '作为': {'作为'.encode('gbk').hex()}")
print()

# Read the first entry as UTF-8 (with replace for errors)
with open('vietnamese-vocab.js', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Find the first vocab line
import re
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'như' in line and 'starter' not in line:
        print(f"Line {i+1}: {repr(line[:120])}")
        # Check if the Chinese part looks correct
        if '作为' in line:
            print("  -> Chinese '作为' found (CORRECT UTF-8)")
        elif any(ord(c) > 0x3000 for c in line):
            # Has Chinese chars but not exact match
            chinese_chars = re.findall(r'[\u4e00-\u9fff]+', line)
            print(f"  -> Chinese chars found: {chinese_chars}")
        break

# Let's also check what the actual bytes say
# Find 'starter: [' and then the first entry
starter_idx = raw.find(b'starter:')
# Find the next newline after starter
nl = raw.find(b'\n', starter_idx)
# Find the opening bracket [
bracket = raw.find(b'[', nl)
# Find the next " after [
quote = raw.find(b'"', bracket)
# Now find the Vietnamese word
end_quote = raw.find(b'"', quote+1)
viet_word = raw[quote+1:end_quote]
print(f"\nFirst vocab word bytes: {viet_word}")
print(f"  As UTF-8: {viet_word.decode('utf-8', errors='replace')}")
print(f"  As Latin-1: {viet_word.decode('latin-1')}")

# Find the Chinese part
# After the first word, there should be comma and space, then the Chinese
after_word = raw.find(b'"', end_quote+1)
before_chinese = raw[end_quote+1:after_word+1]
print(f"Between first and second quote: {before_chinese}")

# Now find the Chinese word (second quoted string)
chinese_start = raw.find(b'"', after_word)
chinese_end = raw.find(b'"', chinese_start+1)
chinese_bytes = raw[chinese_start+1:chinese_end]
print(f"\nChinese part bytes: {chinese_bytes.hex()}")
print(f"  As UTF-8: {chinese_bytes.decode('utf-8', errors='replace')}")
print(f"  As GBK: {chinese_bytes.decode('gbk', errors='replace')}")
