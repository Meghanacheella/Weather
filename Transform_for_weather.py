import json
import os

def save_local_backup(data, folder="daily_backups"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    filename = f"{folder}/{data['city']}_{data['timestamp'].strftime('%Y-%m-%d_%H-%M')}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    
    print(f"Saved local backup: {filename}")
    return filename
