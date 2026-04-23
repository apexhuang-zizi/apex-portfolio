import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('vietnamese-vocab.js', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Check if there's a JS object like: starter: [ ["như", ...], ["tôi", ...], ... ]
# by looking at the raw bytes of specific Vietnamese chars

# Find lines containing the starter array
lines = content.split('\n')
in_starter = False
count = 0
for i, line in enumerate(lines):
    if 'starter:' in line and '[' in line:
        in_starter = True
        print(f"Found starter at line {i+1}: {repr(line[:100])}")
        continue
    if in_starter:
        if line.strip().startswith(']'):
            print(f"Starter section ends at line {i+1}")
            break
        # Count vocab entries
        matches = re.findall(r'\["([^"]+)"', line)
        for m in matches:
            count += 1
            if count <= 5:
                print(f"  Entry {count}: {repr(m)}")
            elif count == 6:
                print(f"  ... (total so far)")

print(f"\nTotal starter entries: {count}")

# Also check basic
in_basic = False
count2 = 0
for i, line in enumerate(lines):
    if 'basic:' in line and '[' in line:
        in_basic = True
        print(f"\nFound basic at line {i+1}: {repr(line[:100])}")
        continue
    if in_basic:
        if line.strip().startswith(']'):
            print(f"Basic section ends at line {i+1}")
            break
        matches = re.findall(r'\["([^"]+)"', line)
        for m in matches:
            count2 += 1
            if count2 <= 3:
                print(f"  Entry {count2}: {repr(m)}")
            elif count2 == 4:
                print(f"  ... (total so far)")

print(f"Total basic entries: {count2}")
