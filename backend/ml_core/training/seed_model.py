import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import joblib

df = pd.read_csv("dataset/seed.csv")

le_country = LabelEncoder()
le_species = LabelEncoder()

df['Country_enc'] = le_country.fit_transform(df['Country'])
df['Species_enc'] = le_species.fit_transform(df['Species'])

X = df[['Country_enc', 'Species_enc', 'Distance_km']]
y = df['Seed_Quality_Rating']

model = RandomForestRegressor(n_estimators=20, random_state=42)
model.fit(X, y)

joblib.dump(model, "models/seed.pkl")
joblib.dump(le_country, "models/le_country_seed.pkl")
joblib.dump(le_species, "models/le_species_seed_chk.pkl")

print("Seed quality model trained successfully!")
