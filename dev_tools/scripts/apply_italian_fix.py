
import json
import re

def fix_italian():
    try:
        with open('patch_fix_italian.json', 'r', encoding='utf-8') as f:
            patch_data = json.load(f)
            italian_data = patch_data.get('it', {})
            print(f"Loaded {len(italian_data)} Italian Translation Keys")
    except Exception as e:
        print(f"Error reading patch file: {e}")
        return

    with open('translations.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    new_lines = []
    inside_it = False
    
    # We will look for the line "    'it': {"
    lang_start_re = re.compile(r"^\s+'([a-z]{2})': \{")
    
    for line in lines:
        match = lang_start_re.match(line)
        if match:
            lang = match.group(1)
            if lang == 'it':
                inside_it = True
                # Rewrite the IT block completely
                new_lines.append(f"    'it': {{\n")
                for k, v in italian_data.items():
                    val_escaped = v.replace("'", "\\'")
                    # Use 8 spaces indentation
                    new_lines.append(f"        '{k}': '{val_escaped}',\n")
                new_lines.append("    },\n")
                continue
            else:
                inside_it = False
        
        if inside_it:
            # Skip lines until closing brace
            if line.strip() == '},':
                inside_it = False
            continue
            
        new_lines.append(line)

    with open('translations.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("translations.py updated with Italian content.")

if __name__ == "__main__":
    fix_italian()
