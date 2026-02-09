from translations import TRANSLATIONS

print("Keys in TRANSLATIONS:", list(TRANSLATIONS.keys()))

if 'pt' in TRANSLATIONS:
    print("\n--- 'pt' keys (first 20) ---")
    keys = list(TRANSLATIONS['pt'].keys())
    print(keys[:20])
    
    print("\n--- Check specific keys in 'pt' ---")
    checks = ['market_global_title', 'disease_title', 'loc_title', 'yield_title', 'btn_start']
    for k in checks:
        print(f"pt - {k}: {TRANSLATIONS['pt'].get(k, 'MISSING')}")

if 'vi' in TRANSLATIONS:
    print("\n--- Check specific keys in 'vi' ---")
    checks = ['market_global_title', 'disease_title', 'loc_title', 'yield_title', 'btn_start']
    for k in checks:
        print(f"vi - {k}: {TRANSLATIONS['vi'].get(k, 'MISSING')}")

# Global check for "GLOBAL MARKET" in all languages to see which ones are still English
print("\n--- Global Check for 'GLOBAL MARKET' ---")
for lang, data in TRANSLATIONS.items():
    val = data.get('market_global_title', 'MISSING')
    print(f"{lang}: {val}")

