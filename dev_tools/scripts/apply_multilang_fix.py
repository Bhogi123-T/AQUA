import json
import re

def apply_patches():
    with open('patch_final_features.json', 'r', encoding='utf-8') as f:
        patches = json.load(f)
    
    with open('translations.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    new_lines = []
    current_lang = None
    lang_pattern = re.compile(r"^\s+'([a-z]{2})': \{")
    
    # We will track which keys we have processed for the current lang to avoid duplicates if we were to insert (but here we are replacing)
    # Actually, simplistic replacement line by line is safer to match existing indentation.
    
    for line in lines:
        match = lang_pattern.match(line)
        if match:
            current_lang = match.group(1)
            
        if current_lang in patches:
            # Check if this line defines a key we want to patch
            key_match = re.search(r"^\s+'([^']+)':", line)
            if key_match:
                key = key_match.group(1)
                if key in patches[current_lang]:
                    val = patches[current_lang][key]
                    # Create new line with same indentation
                    # We assume 8 spaces indentation based on previous files
                    new_line = f"        '{key}': '{val}',\n"
                    new_lines.append(new_line)
                    continue # Skip adding the old line
                    
        new_lines.append(line)
        
    with open('translations.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("Patches applied successfully.")

if __name__ == "__main__":
    apply_patches()
