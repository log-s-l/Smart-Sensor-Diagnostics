#PURPOSE: Lets you safely read and summarize the fault log
#HOW IT WORKS:
# Opens fault_log.csv if it exists
# Functions:
#   get_latest() --> returns the most recent row (latest reading)
#   get_summary() --> returns a quick summary (# of rows, # of faults, last status)

import pandas as pd, os

def get_latest(file="data/fault_log.csv"):
    if not os.path.exists(file):
        return None
    df = pd.read_csv(file)
    return df.iloc[-1].to_dict()

def get_summary(file="data/fault_log.csv"):
    if not os.path.exists(file):
        return {}
    df = pd.read_csv(file)
    return {
        "total_rows": len(df),
        "faults_found": (df["fault_status"] != "OK").sum(),
        "last_status": df["fault_status"].iloc[-1]
    }
