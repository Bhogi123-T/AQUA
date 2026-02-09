
import json
import re
import glob

def apply_patches():
    # Read all patch files
    patches = {}
    for filename in glob.glob('patch_*.json'):
        print(f"Reading {filename}...")
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for lang, updates in data.items():
                    if lang not in patches:
                        patches[lang] = {}
                    patches[lang].update(updates)
        except Exception as e:
            print(f"Error reading {filename}: {e}")

    # Read translations.py
    with open('translations.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    current_lang = None
    
    # Regex to detect start of language block
    lang_pattern = re.compile(r"^\s+'([a-z]{2})': \{")
    
    # Regex to detect key-value pair
    # Matches: "        'key': 'value'," or "        'key': "value","
    kv_pattern = re.compile(r"^\s+'([^']+)':\s*(['\"].*['\"]),?")
    
    for line in lines:
        match = lang_pattern.match(line)
        if match:
            current_lang = match.group(1)
            new_lines.append(line)
            continue
            
        # If inside a language block that we have patches for
        if current_lang and current_lang in patches:
            kv_match = kv_pattern.match(line)
            if kv_match:
                key = kv_match.group(1)
                if key in patches[current_lang]:
                    val = patches[current_lang][key]
                    # Create new line with correct indentation and comma
                    # Escape single quotes in value if we wrap in single quotes
                    val_escaped = val.replace("'", "\\'")
                    new_line = f"        '{key}': '{val_escaped}',\n"
                    new_lines.append(new_line)
                    # Remove from patches to track usage?
                    # patches[current_lang].pop(key)
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    with open('translations.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("All patches applied successfully.")

if __name__ == "__main__":
    apply_patches()
