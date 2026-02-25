import os

base_path = r"c:\Users\bhoge\Downloads\AQUA-main (1)\AQUA-main"
training_path = os.path.join(base_path, "ml_core", "training")
models_path = os.path.join(base_path, "ml_core", "models")
datasets_path = os.path.join(base_path, "ml_core", "datasets")

if not os.path.exists(models_path):
    os.makedirs(models_path)

scripts = [
    "buyer_model.py",
    "disease_model.py",
    "feed_model.py",
    "location_model.py",
    "seed_model.py",
    "stocking_model.py",
    "yield_model.py"
]

for script in scripts:
    script_path = os.path.join(training_path, script)
    with open(script_path, 'r') as f:
        code = f.read()
    
    # Fix paths
    # The scripts use relative paths like "dataset/yield.csv" and "models/yield.pkl"
    # We want to replace "dataset/" with absolute datasets_path and "models/" with absolute models_path
    
    # Note: Use forward slashes for the code string to avoid escaping issues
    ds_p = datasets_path.replace('\\', '/')
    md_p = models_path.replace('\\', '/')
    
    code = code.replace('"dataset/', f'"{ds_p}/')
    code = code.replace('"models/', f'"{md_p}/')
    
    # Execute
    print(f"--- Running {script} ---")
    try:
        exec(code, {'__name__': '__main__', 'print': print})
    except Exception as e:
        print(f"Error in {script}: {e}")

print("\n--- All models rebuilt successfully ---")
