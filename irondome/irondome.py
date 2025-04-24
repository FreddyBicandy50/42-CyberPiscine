import os
import sys
import time
import math
import logging
import daemon
import threading
import psutil
import subprocess
from pathlib import Path
from collections import Counter, defaultdict

LOG_PATH = "/var/log/irondome"
LOG_FILE = os.path.join(LOG_PATH, "irondome.log")
ENTROPY_THRESHOLD = 7.5  # Threshold for high entropy
SCAN_INTERVAL = 60       # Seconds between scans
READ_THRESHOLD = 100     # Number of reads per interval considered abusive
CRYPTO_PROCESSES = ['openssl', 'gpg', 'ssh', 'scp', 'sftp']

def check_root():
    if os.geteuid() != 0:
        print("This program must be run as root.")
        sys.exit(1)

def setup_logging():
    os.makedirs(LOG_PATH, exist_ok=True)
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

def calculate_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = Counter(data)
    length = len(data)
    entropy = -sum((count / length) * math.log2(count / length) for count in counts.values())
    return entropy

def scan_directory_for_entropy(path, threshold=ENTROPY_THRESHOLD):
    suspicious_files = []
    for root, _, files in os.walk(path):
        for fname in files:
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, "rb") as f:
                    data = f.read(2048)  # Read only first 2KB for performance
                    entropy = calculate_entropy(data)
                    if entropy > threshold:
                        suspicious_files.append((fpath, entropy))
            except Exception as e:
                logging.warning(f"Failed to read {fpath}: {e}")
    return suspicious_files

def monitor_entropy(monitored_path):
    while True:
        time.sleep(SCAN_INTERVAL)
        alerts = scan_directory_for_entropy(monitored_path)
        for fpath, entropy in alerts:
            logging.warning(f"High entropy detected: {fpath} (entropy: {entropy:.2f})")

def monitor_disk_reads(monitored_path):
    read_counts = defaultdict(int)
    while True:
        time.sleep(SCAN_INTERVAL)
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                pid = proc.info['pid']
                name = proc.info['name']
                io_counters = proc.io_counters()
                read_bytes = io_counters.read_bytes
                read_counts[pid] = read_bytes
                if read_bytes > READ_THRESHOLD * 1024 * 1024:  # Convert MB to bytes
                    logging.warning(f"Disk read abuse detected: PID {pid} ({name}) read {read_bytes / (1024 * 1024):.2f} MB")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

def monitor_crypto_activity():
    while True:
        time.sleep(SCAN_INTERVAL)
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                name = proc.info['name']
                if name in CRYPTO_PROCESSES:
                    logging.warning(f"Cryptographic activity detected: PID {proc.pid} ({name})")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

def monitor_loop(monitored_path):
    logging.info(f"Irondome started monitoring: {monitored_path}")
    threads = []
    t_entropy = threading.Thread(target=monitor_entropy, args=(monitored_path,))
    t_reads = threading.Thread(target=monitor_disk_reads, args=(monitored_path,))
    t_crypto = threading.Thread(target=monitor_crypto_activity)
    threads.extend([t_entropy, t_reads, t_crypto])
    for t in threads:
        t.daemon = True
        t.start()
    while True:
        time.sleep(1)

def main(monitored_path):
    check_root()
    setup_logging()
    monitor_loop(monitored_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: sudo python3 {sys.argv[0]} <path-to-monitor>")
        sys.exit(1)

    monitored_path = Path(sys.argv[1])
    if not monitored_path.exists() or not monitored_path.is_dir():
        print(f"Invalid directory: {monitored_path}")
        sys.exit(1)

    with daemon.DaemonContext():
        main(monitored_path)
