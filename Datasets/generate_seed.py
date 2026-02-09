import pandas as pd
import random
from faker import Faker

fake = Faker()
rows = []
FISHS = ["Rohu", "Tilapia", "Catfish", "Seabass", "Carp", "Salmon", "Trout", "Pangasius", "Grouper", "Snapper", "Milkfish", "Barramundi", "Tuna", "Cod"]
PRAWNS = ["Vannamei", "Tiger Prawn", "Freshwater Prawn", "Banana Prawn", "King Prawn", "Whiteleg Shrimp", "Black Tiger Shrimp"]
CRABS = ["Mud Crab", "Blue Swimmer Crab", "King Crab", "Snow Crab", "Dungeness Crab", "Soft Shell Crab"]
ALL_SPECIES = FISHS + PRAWNS + CRABS

for _ in range(10000):
    rows.append([
        random.choice(["India","Vietnam","Thailand","Indonesia","Bangladesh"]),
        fake.state(),
        fake.company(),
        random.choice(ALL_SPECIES),
        random.randint(3,5),
        fake.phone_number(),
        round(random.uniform(1,200),1)
    ])

df = pd.DataFrame(rows, columns=["Country","State","Supplier_Name","Species","Seed_Quality_Rating","Contact","Distance_km"])
df.to_csv("dataset/seed.csv", index=False)
print("✅ Ecosystem Seed dataset generated")
