
import json
import re

def fix_bengali():
    try:
        with open('patch_fix_bengali.json', 'r', encoding='utf-8') as f:
            patch_data = json.load(f)
            bengali_data = patch_data.get('bn', {})
            print(f"Loaded {len(bengali_data)} Bengali Translation Keys")
    except Exception as e:
        print(f"Error reading patch file: {e}")
        return

    with open('translations.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    new_lines = []
    inside_bn = False
    
    # We will look for the line "    'bn': {" which we know exists from previous generation
    lang_start_re = re.compile(r"^\s+'([a-z]{2})': \{")
    
    for line in lines:
        match = lang_start_re.match(line)
        if match:
            lang = match.group(1)
            if lang == 'bn':
                inside_bn = True
                # Rewrite the BN block completely
                new_lines.append(f"    'bn': {{\n")
                for k, v in bengali_data.items():
                    val_escaped = v.replace("'", "\\'")
                    # Use 8 spaces indentation
                    new_lines.append(f"        '{k}': '{val_escaped}',\n")
                new_lines.append("    },\n")
                continue
            else:
                inside_bn = False
        
        if inside_bn:
            # Skip lines until closing brace
            if line.strip() == '},':
                inside_bn = False
            continue
            
        new_lines.append(line)

    with open('translations.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("translations.py updated with Bengali content.")

if __name__ == "__main__":
    fix_bengali()
