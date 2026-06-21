import os
import joblib
import warnings

# Suppress sklearn unpickling warnings for cleaner console output
warnings.filterwarnings("ignore", category=UserWarning)

USD_TO_INR = 83.0

GLOBAL_EXCHANGE_RATES = {
    "USD": 1.0,
    "INR": 83.0,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 150.5,
    "AUD": 1.53,
    "CAD": 1.35,
    "VND": 24500, # Vietnam Dong (major aqua player)
    "THB": 35.8,  # Thai Baht
    "IDR": 15600  # Indonesian Rupiah
}

def get_global_prices(usd_amount):
    """Returns a dict of the amount in major global currencies."""
    prices = {}
    for curr, rate in GLOBAL_EXCHANGE_RATES.items():
        val = usd_amount * rate
        # formatting: use 2 decimal places for most, but 0 for large currencies like VND/IDR
        if curr in ["VND", "IDR"]:
            prices[curr] = f"{int(val):,}"
        else:
            prices[curr] = f"{val:,.2f}"
    return prices

def convert_quantity(value, target_unit, from_unit="kg"):
    if from_unit == "grams": value_kg = value / 1000
    elif from_unit == "tons": value_kg = value * 1000
    elif from_unit == "pounds": value_kg = value / 2.20462
    else: value_kg = value
    
    if target_unit == "grams": return value_kg * 1000, "grams (g)"
    elif target_unit == "tons": return value_kg / 1000, "Metric Tons (MT)"
    elif target_unit == "pounds": return value_kg * 2.20462, "Pounds (lbs)"
    else: return value_kg, "Kilograms (kg)"

MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "models"))

def _load_model(fname):
    path = os.path.join(MODEL_DIR, fname)
    if not os.path.exists(path):
        print(f"⚠️  [ML WARNING] Model file missing: {path}. Using Safe Dummy Fallback.")
        class DummyModel:
            def predict(self, *args, **kwargs): return [0]
            def transform(self, *args, **kwargs): return [0]
            @property
            def classes_(self): return []
        return DummyModel()
    try:
        return joblib.load(path)
    except Exception as e:
        print(f"❌ [ML ERROR] Error loading {fname}: {e}. Using Safe Dummy Fallback.")
        class DummyModel:
            def predict(self, *args, **kwargs): return [0]
            def transform(self, *args, **kwargs): return [0]
            @property
            def classes_(self): return []
        return DummyModel()

disease_model = _load_model("disease.pkl")
location_model = _load_model("location.pkl")
feed_model = _load_model("feed.pkl")
yield_model = _load_model("yield.pkl")
buyer_model = _load_model("buyer.pkl")
stocking_model = _load_model("stocking.pkl")
seed_model = _load_model("seed.pkl")

le_country = _load_model("le_country.pkl")
le_state = _load_model("le_state.pkl")
le_climate = _load_model("le_climate.pkl")
le_aqua = _load_model("le_aqua.pkl")
le_species_loc = _load_model("le_species_location.pkl")
le_species_feed = _load_model("le_species_feed.pkl")
le_feed = _load_model("le_feed.pkl")
le_species_yield = _load_model("le_species_yield.pkl")
le_country_buyer = _load_model("le_country_buyer.pkl")
le_species_buyer = _load_model("le_species_buyer.pkl")
le_grade_buyer = _load_model("le_grade_buyer.pkl")
le_species_stock = _load_model("le_species_stock.pkl")
le_soil = _load_model("le_soil.pkl")
le_water_source = _load_model("le_water_source.pkl")
le_season_stock = _load_model("le_season_stock.pkl")
le_country_seed = _load_model("le_country_seed.pkl")
le_species_seed_chk = _load_model("le_species_seed_chk.pkl")
