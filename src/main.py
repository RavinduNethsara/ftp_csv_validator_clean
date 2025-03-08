import os
import generate_csv  # Import the CSV generator
from ftp_handler import connect_ftp, list_files, download_file
from validation import validate_csv

def process_files():
    """Main processing function that downloads, validates, and logs CSV files."""
    
    # ✅ Step 1: Generate test CSVs before downloading
    generate_csv.generate_valid_csv()
    generate_csv.generate_invalid_csv()

    ftp = connect_ftp()
    files = list_files(ftp)
    
    for file in files:
        try:
            if file.endswith(".csv"):  # Download only CSV files
                local_file = download_file(ftp, file)
                
                if local_file:
                    # ✅ Validate CSV before storing
                    if validate_csv(local_file):
                        print(f"✅ Valid CSV file: {local_file}")
                    else:
                        print(f"❌ Invalid CSV file moved to: data/invalid/{file}")
        except Exception as e:
            print(f"Error processing {file}: {e}")
    
    ftp.quit()

if __name__ == "__main__":
    os.makedirs("data/valid", exist_ok=True)
    os.makedirs("data/invalid", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    os.makedirs("data/test", exist_ok=True)  # Test data directory
    process_files()
