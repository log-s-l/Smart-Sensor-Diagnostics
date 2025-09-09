# PURPOSE: Creates fake sensor data and writes it to a CSV log file
# HOW IT WORKS:
# Sets up a CSV file with column headers (time, temperature, voltage, etc.)
# Appends a new row every interval seconds until it reaches max_rows
# Uses time.sleep() to pace the simulation so it feels like a live stream
# *think of as "hardware box" producing sensor readings*

import csv, random, time, os

DATA_FILE = "data/sensor_log.csv"

def simulate_sensors(interval=2):
    os.makedirs("data", exist_ok=True)

    # Overwrite file with headers at start
    with open(DATA_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time", "temperature", "voltage", "current", "vibration"])

    while True:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        row = [
            timestamp,
            round(random.uniform(20, 90), 2),   # temperature
            round(random.uniform(4.0, 6.0), 2), # voltage
            round(random.uniform(0.5, 1.5), 2), # current
            round(random.uniform(0.0, 2.0), 2)  # vibration
        ]

        with open(DATA_FILE, "a", newline="") as f:
            csv.writer(f).writerow(row)

        print(f"✅ Sensor reading at {timestamp}: {row[1:]}")

        time.sleep(interval)

#this ensures safety when simulate_sensors is imported in another file
if __name__ == "__main__":
    random.seed(time.time())  # ensures different sequence each run
    simulate_sensors()
