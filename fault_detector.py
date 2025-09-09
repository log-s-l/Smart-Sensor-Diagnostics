# PURPOSE: Reads the log and checks for problems
# HOW IT WORKS:
# Opens the CSV file with pandas
# Defines safe ranges for each sensor (temperature < 80 C, etc.)
# For each row, it checks values and labels the status as "ok" or with an error message
# Saves the annotated data to a new file (fault_log.csv)
# Uses retry + backoff logic so if the log file isn't ready yet, it waits and retries instead of crashing

import pandas as pd, os, time

THRESHOLDS = {
    "temperature": {"max": 80, "min": 0},
    "voltage": {"max": 5.5, "min": 4.5},
    "current": {"max": 1.2, "min": 0.8},
    "vibration": {"max": 1.5, "min": 0}
}

def check_row(row):
    faults = []
    if row["temperature"] > THRESHOLDS["temperature"]["max"]:
        faults.append("Overheat")
    if row["voltage"] < THRESHOLDS["voltage"]["min"]:
        faults.append("Undervoltage")
    if row["current"] > THRESHOLDS["current"]["max"]:
        faults.append("Overcurrent")
    if row["vibration"] > THRESHOLDS["vibration"]["max"]:
        faults.append("Excess vibration")
    return ", ".join(faults) if faults else "OK"

def run_fault_detector(
    input_file="data/sensor_log.csv",
    output_file="data/fault_log.csv",
    interval=2
):
    print("⚡ Fault detector running...")
    while True:
        if os.path.exists(input_file):
            try:
                df = pd.read_csv(input_file)
                if not df.empty:
                    df["fault_status"] = df.apply(check_row, axis=1)
                    df.to_csv(output_file, index=False)
                    print(f"✅ Fault detection updated → {output_file} ({len(df)} rows)")
            except Exception as e:
                print(f"⚠️ Error reading {input_file}: {e}")
        else:
            print(f"⚠️ Waiting for {input_file}...")

        time.sleep(interval)

if __name__ == "__main__":
    run_fault_detector()
