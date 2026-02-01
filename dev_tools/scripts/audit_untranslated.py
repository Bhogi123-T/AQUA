
from translations import TRANSLATIONS
import json

def find_untranslated():
    base_lang = 'en'
    if base_lang not in TRANSLATIONS:
        print("Error: Base language 'en' not found.")
        return

    base_keys = TRANSLATIONS[base_lang]
    
    untranslated = {}

    for lang, content in TRANSLATIONS.items():
        if lang == base_lang:
            continue
        
        untranslated[lang] = []
        for k, v in content.items():
            if k in base_keys:
                if v == base_keys[k]:
                    # This is likely a fallback I added
                    untranslated[lang].append(k)

    # Print results
    total_untranslated = 0
    for lang, keys in untranslated.items():
        count = len(keys)
        total_untranslated += count
        print(f"--- {lang} ({count} untranslated keys) ---")
        # Print first 5 as samples
        # print(keys[:5]) 

    print(f"\nTotal untranslated keys found: {total_untranslated}")

if __name__ == "__main__":
    find_untranslated()
