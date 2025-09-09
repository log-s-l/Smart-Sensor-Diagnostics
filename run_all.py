import subprocess
import time
import sys
import os

def run_all():
    # Paths to scripts
    emulator = "simulator.py"
    detector = "fault_detector.py"
    dashboard = "live_dashboard.py"

    # Make sure data/ folder exists
    os.makedirs("data", exist_ok=True)

    print("🚀 Starting system...")

    # Start emulator (writes sensor_log.csv)
    print("▶️ Starting sensor emulator...")
    emu_proc = subprocess.Popen([sys.executable, emulator])

    # Start fault detector (reads sensor_log, writes fault_log.csv)
    time.sleep(1)  # small delay so emulator starts first
    print("▶️ Starting fault detector...")
    det_proc = subprocess.Popen([sys.executable, detector])

    # Wait before launching dashboard (buffer only affects dashboard)
    wait_time = 20
    print(f"⏳ Waiting {wait_time}s before starting dashboard...")
    time.sleep(wait_time)

    # Start Streamlit dashboard (opens in browser)
    print("▶️ Starting dashboard...")
    dash_proc = subprocess.Popen(["streamlit", "run", dashboard])

    print("\n✅ All components running!")
    print("   Emulator PID:", emu_proc.pid)
    print("   Detector PID:", det_proc.pid)
    print("   Dashboard PID:", dash_proc.pid)
    print("\nPress Ctrl+C to stop everything.\n")

    try:
        # Wait until user kills script
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down system...")

        # Kill all child processes
        emu_proc.terminate()
        det_proc.terminate()
        dash_proc.terminate()

        print("✅ All processes stopped.")

if __name__ == "__main__":
    run_all()
