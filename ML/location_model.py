# ml/location_model.py
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load dataset
df = pd.read_csv("dataset/location.csv")

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
joblib.dump(model, "models/location.pkl")
joblib.dump(le_country, "models/le_country.pkl")
joblib.dump(le_state, "models/le_state.pkl")
joblib.dump(le_climate, "models/le_climate.pkl")
joblib.dump(le_aqua, "models/le_aqua.pkl")
joblib.dump(le_species, "models/le_species_location.pkl")

print("Location model trained and saved successfully!")
