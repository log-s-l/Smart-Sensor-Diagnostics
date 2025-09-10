# Smart Sensor Diagnostics Simulation
A modular Python system that simulates sensor data, detects faults in real-time, and displays results on a live dashboard.

Think of it as a **mini hardware monitoring pipeline** with simulation, anomaly detection, and visualization.

```bash
.
├── simulator.py        # Generates fake sensor data (temperature, voltage, etc.)
├── fault_detector.py   # Detects anomalies and writes fault logs
├── reader.py           # Safely reads and summarizes the fault log
├── collect_all.py      # Merges multiple sensor logs (if using multiple devices)
├── run_all.py          # Orchestrator: runs emulator, detector, dashboard
├── test_pipeline.py    # Lightweight test harness (simulate + detect 50 rows)
├── live_dashboard.py   # Streamlit dashboard (visualizes fault log)
├── data/               # Stores generated CSV files
│   ├── sensor_log.csv
│   └── fault_log.csv

```

# Features
**- Live Simulation:** simulator.py generates realistic sensor readings.

**- Fault Detection:** flags anomalies (overheat, undervoltage, etc.).

**- Profiles:** Simulate _normal, degraded_ or _failure_ conditions.

**- Safe Reader:** Query the most recent log or get a summary snapshot.

**- Streamlit Dashboard:** Read-time visualization of sensor data and faults.

**- Orchestrator:** One command to launch the whole pipeline.

# Quick Start
**1. Clone the repo**
```bash
git clone https://github.com/log-s-l/Smart-Sensor-Diagnostics.git
cd Smart-Sensor-Diagnostics
```
**2. Install dependencies**
```bash
pip install pandas streamlit
```
**3. Run the full system**
```bash
python run_all.py
```
This will:

- Start the sensor emulator

- Start the fault detector

- Launch the dashboard in the browser

# Dashboard
The dashboard (live_dashboard.py) is built with [Streamlit](https://streamlit.io/).

It shows:

- Live sensor readings

- Fault status indicators

- Historical fault log

Launches automatically when you run run_all.py.

# Configurations
**Fault Thresholds**
Defined in fault_detector.py
```bash
THRESHOLDS = {
    "temperature": {"max": 80, "min": 0},
    "voltage": {"max": 5.5, "min": 4.5},
    "current": {"max": 1.2, "min": 0.8},
    "vibration": {"max": 1.5, "min": 0}
}
```

# Future Improvements
- Add alerting system (e.g., email/text when faults occur)
- Store logs in a database instead of CSV
- More detailed dashboard with fault history timeline

# License
MIT License -- feel free to use, modify, and share.
