
from translations import TRANSLATIONS
import json

def dump_untranslated():
    base_lang = 'en'
    base_keys = TRANSLATIONS[base_lang]
    
    untranslated = {}

    for lang, content in TRANSLATIONS.items():
        if lang == base_lang:
            continue
        
        untranslated[lang] = []
        for k, v in content.items():
            if k in base_keys:
                if v == base_keys[k]:
                    untranslated[lang].append(k)
                    
    with open('remaining_untranslated.json', 'w', encoding='utf-8') as f:
        json.dump(untranslated, f, indent=2)
    
    print("Dumped to remaining_untranslated.json")

if __name__ == "__main__":
    dump_untranslated()
