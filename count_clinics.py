import re

# Read the comprehensive_x_accounts.md file
with open('/Users/achan/.gemini/antigravity/brain/536af507-cc48-4e56-856f-de8069276c4a/comprehensive_x_accounts.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

clinics = []
for line in lines:
    # Look for lines that start with | and contain @ (table rows with clinic data)
    if line.strip().startswith('|') and '@' in line and '---|' not in line and 'クリニック名' not in line:
        parts = line.split('|')
        if len(parts) >= 3:
            # Extract clinic name (remove ** markers if present)
            name = parts[1].strip().replace('**', '').strip()
            # Extract account part
            account_part = parts[2].strip()
            # Find first @account pattern
            account_match = re.search(r'@(\w+)', account_part)
            if account_match and name:
                account = account_match.group(1)
                # Skip if it's a duplicate
                if (name, account) not in clinics:
                    clinics.append((name, account))

print(f"Total clinics found in comprehensive_x_accounts.md: {len(clinics)}")
print("\nFirst 30 clinics:")
for i, (name, account) in enumerate(clinics[:30], 1):
    print(f"{i}. {name} - @{account}")

if len(clinics) > 30:
    print(f"\n... and {len(clinics) - 30} more")

# Save all clinics to a file for comparison
with open('/Users/achan/.gemini/antigravity/brain/536af507-cc48-4e56-856f-de8069276c4a/all_clinics_from_md.txt', 'w', encoding='utf-8') as f:
    for name, account in clinics:
        f.write(f"{name}\t@{account}\n")

print(f"\nSaved all {len(clinics)} clinics to all_clinics_from_md.txt")

# Now compare with what's in index.html
print("\n" + "="*60)
print("Comparing with index.html...")

with open('/Users/achan/名称未設定フォルダ/campaign-feed-demo/index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Extract clinics from JavaScript array in index.html
html_clinics = []
in_clinics_array = False
for line in html_content.split('\n'):
    if 'const allClinics = [' in line:
        in_clinics_array = True
    elif in_clinics_array and '];' in line:
        break
    elif in_clinics_array and 'name:' in line:
        name_match = re.search(r'name:\s*"([^"]+)"', line)
        if name_match:
            html_clinics.append(name_match.group(1))

print(f"Clinics in index.html: {len(html_clinics)}")
print(f"Clinics in comprehensive_x_accounts.md: {len(clinics)}")
print(f"Difference: {len(clinics) - len(html_clinics)} clinics missing from website")

# Find missing clinics
md_names = set([name for name, _ in clinics])
html_names = set(html_clinics)
missing = md_names - html_names

if missing:
    print(f"\nMissing {len(missing)} clinics from website:")
    for i, name in enumerate(sorted(missing)[:20], 1):
        # Find account for this clinic
        account = next((acc for n, acc in clinics if n == name), "")
        print(f"{i}. {name} - @{account}")
    if len(missing) > 20:
        print(f"... and {len(missing) - 20} more")
