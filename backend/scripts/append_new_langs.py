
import json

def append_new_langs():
    # Load all patches
    patches = {}
    
    # 1. Tamil (Manual high quality)
    try:
        with open('patch_new_langs_1.json', 'r', encoding='utf-8') as f:
            patches.update(json.load(f))
    except: pass
    
    # 2. Others (Auto-generated/Full)
    try:
        with open('patch_new_langs_full.json', 'r', encoding='utf-8') as f:
            full_data = json.load(f)
            # Update patches, respectful of manual overrides if I had any
            for lang, data in full_data.items():
                if lang not in patches:
                    patches[lang] = data
                else:
                    patches[lang].update(data)
    except: pass

    # Read translations.py
    with open('translations.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Remove last closing brace '}' to append new items
    # We essentially look for the last '}' and replace it with our new blocks
    
    content_str = "".join(lines)
    rindex = content_str.rfind('}')
    if rindex == -1:
        print("Error: Could not find closing brace.")
        return

    # Cut off the detailed end
    new_content = content_str[:rindex]
    
    # Append each new language block
    for lang_code, translations in patches.items():
        print(f"Appending {lang_code}...")
        block_str = f"    '{lang_code}': {{\n"
        for k, v in translations.items():
            # Escape single quotes
            val_escaped = v.replace("'", "\\'")
            block_str += f"        '{k}': '{val_escaped}',\n"
        block_str += "    },\n"
        new_content += block_str
        
    # Add closing brace back
    new_content += "}\n"
    
    with open('translations.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print("translations.py updated with new languages.")

if __name__ == "__main__":
    append_new_langs()
