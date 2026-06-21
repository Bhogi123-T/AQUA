import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

# Define relative paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, "datasets", "location.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")

# Load dataset
if not os.path.exists(DATASET_PATH):
    raise FileNotFoundError(f"Dataset not found: {DATASET_PATH}")

df = pd.read_csv(DATASET_PATH)

# Encode categorical columns
le_country = LabelEncoder()
le_state = LabelEncoder()
le_climate = LabelEncoder()
le_aqua = LabelEncoder()
le_species = LabelEncoder()

df['Country_enc'] = le_country.fit_transform(df['Country'])
df['State_enc'] = le_state.fit_transform(df['State'])
df['Climate_enc'] = le_climate.fit_transform(df['Climate_Zone'])
df['Aqua_enc'] = le_aqua.fit_transform(df['Aqua_Type'])
df['Species_enc'] = le_species.fit_transform(df['Species'])

X = df[['Country_enc', 'State_enc', 'Climate_enc', 'Aqua_enc', 'Species_enc']]
y = df['Suitability_Score']

# Train model (using regressor for score)
model = RandomForestRegressor(n_estimators=20, random_state=42)
model.fit(X, y)

# Save model and encoders
os.makedirs(MODEL_DIR, exist_ok=True)
joblib.dump(model, os.path.join(MODEL_DIR, "location.pkl"))
joblib.dump(le_country, os.path.join(MODEL_DIR, "le_country.pkl"))
joblib.dump(le_state, os.path.join(MODEL_DIR, "le_state.pkl"))
joblib.dump(le_climate, os.path.join(MODEL_DIR, "le_climate.pkl"))
joblib.dump(le_aqua, os.path.join(MODEL_DIR, "le_aqua.pkl"))
joblib.dump(le_species, os.path.join(MODEL_DIR, "le_species_location.pkl"))

print(f"Location model and encoders trained and saved successfully to {MODEL_DIR}")
