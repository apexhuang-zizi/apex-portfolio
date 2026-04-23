import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('vietnamese-vocab.js', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

lines = content.split('\n')
in_starter = False
for i, line in enumerate(lines):
    if 'starter:' in line and '[' in line:
        in_starter = True
        continue
    if in_starter:
        if line.strip().startswith(']'):
            break
        # Print the full line
        if line.strip().startswith('['):
            print(f"L{i+1}: {line.rstrip()}")

print("\n=== 检查词库中的特殊字符 ===")
# Check Vietnamese special chars
viet_chars = ['ư', 'ơ', 'ê', 'ô', 'ă', 'â', 'á', 'à', 'ả', 'ã', 'ạ', 'ắ', 'ằ', 'ẳ', 'ẵ', 'ặ', 'é', 'è', 'ẻ', 'ẽ', 'ẹ', 'ế', 'ề', 'ể', 'ễ', 'ệ', 'í', 'ì', 'ỉ', 'ĩ', 'ị', 'ó', 'ò', 'ỏ', 'õ', 'ọ', 'ố', 'ồ', 'ổ', 'ỗ', 'ộ', 'ớ', 'ờ', 'ở', 'ỡ', 'ợ', 'ú', 'ù', 'ủ', 'ũ', 'ụ', 'ứ', 'ừ', 'ử', 'ữ', 'ự', 'ý', 'ỳ', 'ỷ', 'ỹ', 'ỵ', 'đ']
found_chars = set()
all_text = content
for c in viet_chars:
    if c in all_text:
        found_chars.add(c)

print("Vietnamese chars found in vocab:", sorted(found_chars))
print()

# Check for entries that might have wrong encoding
# Look at bytes of a specific entry
import re
matches = re.findall(r'\["([^"]+)"', content)
print(f"Total vocab entries across all levels: {len(matches)}")

# Check entries with special Vietnamese diacritics
special_entries = [m for m in matches if any(c in m for c in 'ươêôăâ')]
print(f"Entries with diacritics: {len(special_entries)}")
for e in special_entries[:10]:
    print(f"  {repr(e)}")
