import pandas as pd
import random

rows = []
FISHS = ["Rohu", "Tilapia", "Catfish", "Seabass", "Carp", "Salmon", "Trout", "Pangasius", "Grouper", "Snapper", "Milkfish", "Barramundi", "Tuna", "Cod"]
PRAWNS = ["Vannamei", "Tiger Prawn", "Freshwater Prawn", "Banana Prawn", "King Prawn", "Whiteleg Shrimp", "Black Tiger Shrimp"]
CRABS = ["Mud Crab", "Blue Swimmer Crab", "King Crab", "Snow Crab", "Dungeness Crab", "Soft Shell Crab"]
ALL_SPECIES = FISHS + PRAWNS + CRABS

for _ in range(10000):
    rows.append([
        random.choice(ALL_SPECIES),
        round(random.uniform(0.5,5),2),
        random.choice(["Clay","Loamy","Sandy"]),
        random.choice(["Canal","River","Borewell"]),
        random.choice(["Summer","Monsoon","Winter"]),
        random.randint(2000,50000),
        round(random.uniform(70,95),2)
    ])

df = pd.DataFrame(rows, columns=["Species","Pond_Area","Soil_Type","Water_Source","Season","Recommended_Stocking","Survival_Rate"])
df.to_csv("dataset/stocking.csv", index=False)
print("✅ Ecosystem Stocking dataset generated")
