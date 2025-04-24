#!/usr/bin/env python3

import os
import sys
import time
import psutil
import logging
import threading
import math
import hashlib
import base64

# Setup logging
LOG_DIR = "/var/log/irondome"
LOG_FILE = os.path.join(LOG_DIR, "irondome.log")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s")

# Globals
READ_THRESHOLD_MB = 100
ENTROPY_THRESHOLD = 6.5
SCAN_INTERVAL = 60  # seconds
MONITORED_DIR = None

# Ignore list
IGNORED_PROCESSES = {'systemd', 'packagekitd', 'rsyslogd', 'bash', 'chrome', 'code', 'python3'}

# === Entropy detection ===
def calculate_entropy(filepath):
    try:
        with open(filepath, 'rb') as f:
            data = f.read(4096)
        if not data:
            return 0.0
        byte_counts = [0] * 256
        for b in data:
            byte_counts[b] += 1
        entropy = 0
        for count in byte_counts:
            if count == 0:
                continue
            p = count / len(data)
            entropy -= p * math.log2(p)
        return entropy
    except Exception:
        return 0.0

def entropy_watcher():
    scanned_files = {}
    while True:
        for root, dirs, files in os.walk(MONITORED_DIR):
            for name in files:
                path = os.path.join(root, name)
                try:
                    entropy = calculate_entropy(path)
                    if path not in scanned_files:
                        scanned_files[path] = entropy
                    else:
                        old_entropy = scanned_files[path]
                        if abs(entropy - old_entropy) > 1.5 and entropy > ENTROPY_THRESHOLD:
                            logging.warning(f"Entropy spike detected: {path} new entropy: {entropy:.2f}")
                            scanned_files[path] = entropy
                except Exception:
                    continue
        time.sleep(SCAN_INTERVAL)

# === Disk read abuse detection ===
def disk_abuse_watcher():
    while True:
        for proc in psutil.process_iter(['pid', 'name', 'io_counters', 'open_files']):
            try:
                name = proc.info['name']
                if name in IGNORED_PROCESSES:
                    continue

                io = proc.info['io_counters']
                if io and io.read_bytes > READ_THRESHOLD_MB * 1024 * 1024:
                    open_files = proc.info['open_files'] or []
                    if any(f.path.startswith(MONITORED_DIR) for f in open_files):
                        read_mb = io.read_bytes / (1024 * 1024)
                        logging.warning(f"Disk read abuse detected: PID {proc.pid} ({name}) read {read_mb:.2f} MB")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        time.sleep(SCAN_INTERVAL)

# === Crypto detection (simple hashing loop detection) ===
def crypto_activity_watcher():
    sample = b"test_data_to_hash"
    count = 0
    start = time.time()
    while True:
        for _ in range(100000):
            hashlib.sha256(sample).digest()
        count += 1
        if time.time() - start > 10:
            if count > 10:
                logging.warning("Intensive cryptographic activity detected.")
            count = 0
            start = time.time()
        time.sleep(1)

# === Main ===
def main():
    global MONITORED_DIR

    if os.geteuid() != 0:
        print("This program must be run as root.")
        sys.exit(1)

    if len(sys.argv) != 2:
        print("Usage: sudo python3 irondome.py <directory_to_monitor>")
        sys.exit(1)

    MONITORED_DIR = os.path.abspath(sys.argv[1])
    if not os.path.isdir(MONITORED_DIR):
        print("Invalid directory to monitor.")
        sys.exit(1)

    logging.info(f"Irondome started monitoring: {MONITORED_DIR}")

    threads = [
        threading.Thread(target=disk_abuse_watcher, daemon=True),
        threading.Thread(target=crypto_activity_watcher, daemon=True),
        threading.Thread(target=entropy_watcher, daemon=True)
    ]

    for t in threads:
        t.start()

    # Keep alive
    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()
