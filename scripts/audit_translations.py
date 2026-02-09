
from translations import TRANSLATIONS

def audit_translations():
    base_lang = 'en'
    if base_lang not in TRANSLATIONS:
        print("Error: Base language 'en' not found.")
        return

    base_keys = set(TRANSLATIONS[base_lang].keys())
    
    missing_report = {}

    for lang, content in TRANSLATIONS.items():
        if lang == base_lang:
            continue
        
        lang_keys = set(content.keys())
        missing = base_keys - lang_keys
        
        if missing:
            missing_report[lang] = list(missing)

    for lang, keys in missing_report.items():
        print(f"Missing keys in '{lang}': {len(keys)}")
        for key in sorted(keys):
            print(f"  - {key}")

if __name__ == "__main__":
    audit_translations()
