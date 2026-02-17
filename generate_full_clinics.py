import re

# Read comprehensive_x_accounts.md to get all clinics
with open('/Users/achan/.gemini/antigravity/brain/536af507-cc48-4e56-856f-de8069276c4a/comprehensive_x_accounts.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

clinics_dict = {}  # Use dict to avoid duplicates
for line in lines:
    if line.strip().startswith('|') and '@' in line and '---|' not in line and 'クリニック名' not in line:
        parts = line.split('|')
        if len(parts) >= 3:
            name = parts[1].strip().replace('**', '').strip()
            account_part = parts[2].strip()
            account_match = re.search(r'@(\w+)', account_part)
            if account_match and name:
                account = account_match.group(1)
                # Use name as key to avoid duplicates
                if name not in clinics_dict:
                    clinics_dict[name] = account

# Convert to list and sort
clinics = [(name, account) for name, account in clinics_dict.items()]
clinics_sorted = sorted(clinics, key=lambda x: x[0])

# Generate JavaScript array
js_array = "        const allClinics = [\n"
for name, account in clinics_sorted:
    js_array += f'            {{name: "{name}", account: "@{account}"}},\n'
js_array += "        ];"

# Save to file
with open('/Users/achan/名称未設定フォルダ/campaign-feed-demo/updated_clinics_array.js', 'w', encoding='utf-8') as f:
    f.write(js_array)

print(f"Generated JavaScript array with {len(clinics_sorted)} unique clinics")
print(f"Saved to updated_clinics_array.js")
print(f"\nFirst 10 clinics in sorted order:")
for i, (name, account) in enumerate(clinics_sorted[:10], 1):
    print(f"{i}. {name} - @{account}")
