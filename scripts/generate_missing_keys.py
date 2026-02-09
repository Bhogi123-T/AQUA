
from translations import TRANSLATIONS
import json

def generate_missing_blocks():
    base_lang = 'en'
    base_keys = TRANSLATIONS[base_lang]
    
    with open('missing_patches.txt', 'w', encoding='utf-8') as f:
        for lang, content in TRANSLATIONS.items():
            if lang == base_lang:
                continue
            
            existing_keys = set(content.keys())
            missing_keys = [k for k in base_keys.keys() if k not in existing_keys]
            
            if missing_keys:
                f.write(f"=== {lang} ===\n")
                # We need to find the last key in the existing dict to know where to insert?
                # Actually, simply appending before the closing brace is safer.
                # So we just list the keys and values to append.
                for k in missing_keys:
                    val = base_keys[k]
                    val = val.replace("'", "\\'") # Simple escape
                    f.write(f"        '{k}': '{val}',\n")
                f.write(f"=== END {lang} ===\n\n")

if __name__ == "__main__":
    generate_missing_blocks()
