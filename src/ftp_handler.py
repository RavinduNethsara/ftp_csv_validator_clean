import ftplib
import os

FTP_SERVER = "ftp.ncbi.nlm.nih.gov"
FTP_USER = "anonymous"
FTP_PASS = "anonymous@domain.com"
LOCAL_STORAGE = "data/valid"
TRACKED_FILES_LOG = "logs/downloaded_files.txt"

def connect_ftp():
    """Establish FTP connection to NCBI FTP Server."""
    try:
        ftp = ftplib.FTP()
        ftp.connect(FTP_SERVER, 21, timeout=10)  # Explicitly set port 21
        ftp.login(FTP_USER, FTP_PASS)
        ftp.set_pasv(True)  # Enable passive mode
        print("Connected to FTP Server:", FTP_SERVER)
        return ftp
    except ftplib.all_errors as e:
        print(f"FTP Connection Error: {e}")
        return None

def list_files(ftp):
    """List files in the NCBI FTP directory."""
    try:
        ftp.cwd("pub/pmc")  # Change directory where CSV files exist
        files = ftp.nlst()
        print("Files available on FTP Server:", files)
        return files
    except ftplib.all_errors as e:
        print(f"Error listing files: {e}")
        return []

def is_file_downloaded(filename):
    """Check if a file has already been downloaded."""
    if os.path.exists(TRACKED_FILES_LOG):
        with open(TRACKED_FILES_LOG, 'r') as f:
            downloaded_files = f.read().splitlines()
        return filename in downloaded_files
    return False

def log_downloaded_file(filename):
    """Log downloaded files to prevent duplicates."""
    with open(TRACKED_FILES_LOG, 'a') as f:
        f.write(filename + "\n")

def download_file(ftp, filename):
    """Download a file from the FTP server if it hasn't been downloaded before."""
    local_path = os.path.join(LOCAL_STORAGE, filename)
    
    if os.path.exists(local_path) or is_file_downloaded(filename):
        print(f"Skipping {filename}, already downloaded.")
        return None

    try:
        with open(local_path, 'wb') as f:
            ftp.retrbinary(f"RETR {filename}", f.write)
        log_downloaded_file(filename)  # Track the downloaded file
        print(f"Downloaded: {filename}")
        return local_path
    except ftplib.all_errors as e:
        print(f"Error downloading {filename}: {e}")
        return None
