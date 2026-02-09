
import json
from translations import TRANSLATIONS

# Map of language codes to a "simulated" translation suffix or known value
# In a real scenario, this would call a translation API.
# Here we will use English as base + [Lang Code] to denote it exists, 
# ensuring the app doesn't crash, and fill common terms.

LANG_NAMES = {
    "bn": "Bengali", "vi": "Vietnamese", "id": "Indonesian",
    "sw": "Swahili", "ha": "Hausa", "it": "Italian",
    "pt": "Portuguese", "mi": "Maori"
}

# Some static known translations for polish
STATIC_TRANS = {
    "bn": {"nav_farmer": "কৃষক হাব", "login": "লগইন", "logout": "লগআউট", "btn_start": "শুরু করুন"},
    "vi": {"nav_farmer": "Trung tâm Nông dân", "login": "Đăng nhập", "logout": "Đăng xuất", "btn_start": "Bắt đầu"},
    "id": {"nav_farmer": "Hub Petani", "login": "Masuk", "logout": "Keluar", "btn_start": "Mulai"},
    "sw": {"nav_farmer": "Kitovu cha Wakulima", "login": "Ingia", "logout": "Toka", "btn_start": "Anza"},
    "ha": {"nav_farmer": "Cibiyar Manoma", "login": "Shiga", "logout": "Fita", "btn_start": "Fara"},
    "it": {"nav_farmer": "Hub Agricoltori", "login": "Accedi", "logout": "Esci", "btn_start": "Inizia"},
    "pt": {"nav_farmer": "Hub do Agricultor", "login": "Entrar", "logout": "Sair", "btn_start": "Começar"},
    "mi": {"nav_farmer": "Punyenga Kaipāmu", "login": "Takiuru", "logout": "Takiputa", "btn_start": "Tīmata"}
}

def generate_full_patch():
    base_keys = TRANSLATIONS['en']
    full_patch = {}

    for code in LANG_NAMES.keys():
        full_patch[code] = {}
        for k, v in base_keys.items():
            # Use static translation if available
            if code in STATIC_TRANS and k in STATIC_TRANS[code]:
                full_patch[code][k] = STATIC_TRANS[code][k]
            else:
                # Fallback: English value (simulating translation request)
                # Ideally, the user would provide these or we'd use an API.
                # For now, we populate with English to prevent missing keys.
                full_patch[code][k] = v

    with open('patch_new_langs_full.json', 'w', encoding='utf-8') as f:
        json.dump(full_patch, f, indent=2)
    
    print("Generated patch_new_langs_full.json")

if __name__ == "__main__":
    generate_full_patch()
