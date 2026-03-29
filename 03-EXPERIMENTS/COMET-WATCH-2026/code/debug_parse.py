import re

with open('3I_ATLAS_vectors.txt', 'r') as f:
    content = f.read()

# Try simpler pattern for dates
pattern = r'(\d+\.\d+).*?A\.D\.\s+(\d{4}-\w{3}-\d{1,2}).*?TDB'
matches = re.findall(pattern, content, re.DOTALL)
print(f'Found {len(matches)} date matches')
for m in matches[:5]:
    print(f'  JD={m[0]}, Date={m[1]}')
