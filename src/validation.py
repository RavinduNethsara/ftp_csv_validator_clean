import os
import pandas as pd
import requests  # External API request for GUID
from datetime import datetime

ERROR_STORAGE = "data/invalid"
LOG_FILE = "logs/error_log.txt"
UUID_API_URL = "https://www.uuidtools.com/api/generate/v1"

def fetch_guid():
    """Fetch a GUID from an external API."""
    try:
        response = requests.get(UUID_API_URL)
        if response.status_code == 200:
            return response.json()[0]  # API returns a list, we take the first GUID
        else:
            print("⚠️ Failed to fetch GUID, using local UUID instead.")
            return str(uuid.uuid4())  # Fallback to local UUID
    except Exception as e:
        print(f"⚠️ Error fetching GUID: {e}")
        return str(uuid.uuid4())  # Fallback to local UUID

def validate_csv(file_path):
    """Validate CSV file contents based on assignment requirements."""
    try:
        df = pd.read_csv(file_path)

        # ✅ Expected headers
        expected_headers = ["batch_id", "timestamp"] + [f"reading{i}" for i in range(1, 11)]
        if list(df.columns) != expected_headers:
            raise ValueError("Incorrect headers found")

        # ✅ Check for duplicate batch_id values
        if df["batch_id"].duplicated().any():
            raise ValueError("Duplicate batch_id found in file")

        # ✅ Ensure all readings are between 0 and 9.9
        if df.iloc[:, 2:].isnull().any().any() or (df.iloc[:, 2:] > 9.9).any().any():
            raise ValueError("Invalid reading values detected")

        return True
    except Exception as e:
        log_error(file_path, str(e))
        return False

def log_error(file_path, error_message):
    """Log errors in an error log file and move invalid files."""
    error_id = fetch_guid()  # Get GUID from API
    new_path = os.path.join(ERROR_STORAGE, os.path.basename(file_path))
    os.rename(file_path, new_path)
    
    with open(LOG_FILE, 'a') as log:
        log.write(f"{datetime.now()} | {error_id} | {os.path.basename(file_path)} | {error_message}\n")
    
    print(f"❌ Logged error for {file_path}: {error_message}")