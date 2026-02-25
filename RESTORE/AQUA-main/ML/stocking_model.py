import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import joblib

df = pd.read_csv("dataset/stocking.csv")

le_species = LabelEncoder()
le_soil = LabelEncoder()
le_water = LabelEncoder()
le_season = LabelEncoder()

df['Species_enc'] = le_species.fit_transform(df['Species'])
df['Soil_enc'] = le_soil.fit_transform(df['Soil_Type'])
df['Water_enc'] = le_water.fit_transform(df['Water_Source'])
df['Season_enc'] = le_season.fit_transform(df['Season'])

X = df[['Species_enc', 'Pond_Area', 'Soil_enc', 'Water_enc', 'Season_enc']]
y = df[['Recommended_Stocking', 'Survival_Rate']]

model = RandomForestRegressor(n_estimators=20, random_state=42)
model.fit(X, y)

joblib.dump(model, "models/stocking.pkl")
joblib.dump(le_species, "models/le_species_stock.pkl")
joblib.dump(le_soil, "models/le_soil.pkl")
joblib.dump(le_water, "models/le_water_source.pkl")
joblib.dump(le_season, "models/le_season_stock.pkl")

print("Stocking model trained successfully!")
