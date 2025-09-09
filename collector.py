#PURPOSE: If you had multiple sensors or devices, it combines their logs into one file
#HOW IT WORKS:
# uses glob to find all files that match data/sensor*.csv
# Reads them with pandas and concatenates them into one big table
# Saves to combined.csv

import pandas as pd, glob, os

def collect_all(input_pattern="data/sensor*.csv", output_file="data/combined.csv"):
    files = glob.glob(input_pattern)
    if not files:
        print("⚠️ No sensor files found.")
        return

    combined = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    combined.to_csv(output_file, index=False)
    print(f"✅ Collected {len(files)} logs into {output_file}")
