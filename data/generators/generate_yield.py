import pandas as pd
import random

rows = []
FISHS = ["Rohu", "Tilapia", "Catfish", "Seabass", "Carp", "Salmon", "Trout", "Pangasius", "Grouper", "Snapper", "Milkfish", "Barramundi", "Tuna", "Cod"]
PRAWNS = ["Vannamei", "Tiger Prawn", "Freshwater Prawn", "Banana Prawn", "King Prawn", "Whiteleg Shrimp", "Black Tiger Shrimp"]
CRABS = ["Mud Crab", "Blue Swimmer Crab", "King Crab", "Snow Crab", "Dungeness Crab", "Soft Shell Crab"]
ALL_SPECIES = FISHS + PRAWNS + CRABS

for _ in range(10000):
    yield_tons = round(random.uniform(2,10),2)
    rows.append([
        random.choice(ALL_SPECIES),
        round(random.uniform(0.5,5),1),
        random.randint(500,5000),
        random.randint(90,180),
        yield_tons
    ])

df = pd.DataFrame(rows, columns=["Species","Pond_Area","Feed_Used","Culture_Days","Expected_Yield"])
df.to_csv("dataset/yield.csv", index=False)
print("✅ Ecosystem Yield dataset generated")
