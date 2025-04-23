# 🕶️ Stockholm

A simple file encryption and decryption program written in Python using AES-CBC encryption.  
Inspired by ransomware behavior for educational purposes only.

> ⚠️ For educational use only. Do **not** use this software for malicious purposes.

---

## 📦 Features

- Encrypts all files in a specified directory (`~/infection`) with AES-128-CBC
- Appends `.ft` to encrypted files and deletes the original
- Decrypts previously encrypted files using a saved encryption key
- CLI interface with custom options for reverse (decrypt), version, and help

---

## 🧪 How It Works

- When encrypting, the tool:
  - Generates a random 16-byte key (displayed in the terminal — **save it!**)
  - Encrypts each file in the `~/infection` directory
  - Stores the IV and encrypted data in a `.ft` file
  - Deletes the original

- When decrypting, the tool:
  - Takes a 32-character hex key (same one from encryption)
  - Looks for `.ft` files in `~/infection`
  - Extracts the IV and decrypts the data
  - Restores the original file and deletes the `.ft`

---

## 🚀 Usage

```bash
# Encrypt files
$ python3 stockholm.py

[+] Encryption key (save this!): 81acf88ea8374860d0d3f992292356cc

# Decrypt files
$ python3 stockholm.py -r 81acf88ea8374860d0d3f992292356cc
