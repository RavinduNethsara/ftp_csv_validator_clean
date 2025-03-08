import os
import pandas as pd
import random
from datetime import datetime

TEST_DATA_DIR = "data/test"

# Ensure test data directory exists
os.makedirs(TEST_DATA_DIR, exist_ok=True)

def generate_valid_csv():
    """Generate a valid sample CSV file."""
    filename = f"{TEST_DATA_DIR}/MED_DATA_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
    
    data = {
        "batch_id": list(range(1, 11)),
        "timestamp": ["14:01:04"] * 10,
    }
    for i in range(1, 11):  # Readings 1-10
        data[f"reading{i}"] = [round(random.uniform(0, 9.9), 3) for _ in range(10)]

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"✅ Generated valid CSV: {filename}")

def generate_invalid_csv():
    """Generate an invalid CSV file with missing headers and duplicate batch IDs."""
    filename = f"{TEST_DATA_DIR}/BAD_DATA_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"

    data = {
        "batch": list(range(1, 6)) + list(range(1, 6)),  # Duplicate batch IDs
        "time": ["14:01:04"] * 10,
        "reading1": [round(random.uniform(10, 20), 3) for _ in range(10)],  # Invalid values > 9.9
    }

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"❌ Generated invalid CSV: {filename}")

if __name__ == "__main__":
    generate_valid_csv()
    generate_invalid_csv()
