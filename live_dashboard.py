# PURPOSE: Provides a visual dashboard in the browser
# HOW IT WORKS:
# Uses Streamlit to create a live web UI
# Reads the fault log (fault_log.csv) continuously
# Displays line charts of sensor data with OK zones
# Shows the latest fault status
# Refreshes every 2 seconds

import streamlit as st
import pandas as pd
import altair as alt
import os, time

DATA_FILE = "data/fault_log.csv"

# OK thresholds for each sensor
THRESHOLDS = {
    "temperature": {"max": 80, "min": 0},
    "voltage": {"max": 5.5, "min": 4.5},
    "current": {"max": 1.2, "min": 0.8},
    "vibration": {"max": 1.5, "min": 0},
}

st.set_page_config(page_title="Smart Sensor Dashboard", layout="wide")
st.title("Smart Sensor Diagnostics Dashboard")

# Sidebar controls
st.sidebar.header("Controls")
selected_sensors = st.sidebar.multiselect(
    "Select sensors to display",
    ["temperature", "voltage", "current", "vibration"],
    default=["temperature", "voltage", "current", "vibration"]
)

show_faults_only = st.sidebar.checkbox("Show only fault rows", value=False)

# Main dashboard layout
col1, col2, col3 = st.columns(3)
placeholder_chart = st.empty()
placeholder_table = st.empty()

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)

    if not df.empty:
        # Apply fault filter
        if show_faults_only:
            df_display = df[df["fault_status"] != "OK"]
        else:
            df_display = df

        latest = df_display.iloc[-1]

        # Status indicator
        status = latest["fault_status"]
        if status == "OK":
            col1.success("System Healthy")
        else:
            col1.error(f"Fault: {status}")

        # Summary metrics
        col2.metric("Avg Temp (last 10)", round(df["temperature"].tail(10).mean(), 2))
        col3.metric("Total Faults", (df["fault_status"] != "OK").sum())

        # Line chart with selected sensors (Altair with OK zones)
        if selected_sensors:
            charts = []
            for sensor in selected_sensors:
                base = df_display.reset_index()

                # Line chart for sensor values
                line = alt.Chart(base).mark_line().encode(
                    x="index",
                    y=alt.Y(sensor, title=sensor.capitalize()),
                    tooltip=[sensor, "fault_status"]
                ).properties(
                    width=300,
                    height=200,
                    title=f"{sensor.capitalize()} Trend"
                )

                # Shaded OK band
                ok_band = alt.Chart(base).mark_area(
                    opacity=0.2, color="green"
                ).encode(
                    x="index",
                    y=alt.Y(f"{sensor}_min:Q", title=sensor.capitalize()),
                    y2=f"{sensor}_max:Q"
                ).transform_calculate(
                    **{
                        f"{sensor}_min": str(THRESHOLDS[sensor]["min"]),
                        f"{sensor}_max": str(THRESHOLDS[sensor]["max"]),
                    }
                )

                charts.append(ok_band + line)

            # Stack charts vertically
            final_chart = alt.vconcat(*charts)
            placeholder_chart.altair_chart(final_chart, use_container_width=True)

        # Fault history table (last 10 rows)
        placeholder_table.dataframe(df_display.tail(10))

        # Download button
        st.download_button(
            label="Download Fault Log",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="fault_log.csv",
            mime="text/csv",
            key="download_log_button"  # unique key
        )

    else:
        st.warning("No data yet...")
else:
    st.info("Waiting for data...")

time.sleep(2)
