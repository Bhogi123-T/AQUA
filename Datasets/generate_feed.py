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
        random.randint(10,150),
        round(random.uniform(20,32),1),
        round(random.uniform(4,8),1),
        random.choice(["Pellet","Floating","Sinking"]),
        random.randint(28,45),
        round(random.uniform(1,50), 2)
    ])

df = pd.DataFrame(rows, columns=["Species","Age_Days","Water_Temp","DO","Feed_Type","Protein","Feed_Quantity"])
df.to_csv("dataset/feed.csv", index=False)
print("✅ Ecosystem Feed dataset generated")
