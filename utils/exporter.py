import pandas as pd
from datetime import datetime
import os
from config import CSV_FILE_PATH

def export_to_csv(data):
    if not data:
        print("⚠️ No data to export.")
        return

    # Add timestamp to each row
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for row in data:
        row["Timestamp"] = timestamp

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Create data folder if it doesn't exist
    os.makedirs(os.path.dirname(CSV_FILE_PATH), exist_ok=True)

    # Append to CSV
    if not os.path.exists(CSV_FILE_PATH):
        df.to_csv(CSV_FILE_PATH, index=False)
    else:
        df.to_csv(CSV_FILE_PATH, mode='a', header=False, index=False)

    print(f"📁 Data exported to {CSV_FILE_PATH}")
