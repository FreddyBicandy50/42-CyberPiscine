# ARP Poison

## 🐍 ARP Spoofing Tool (Educational)

Implements ARP poisoning to intercept traffic between two hosts.  
Follows the spec: parse command-line input (IP/MAC source/destination), enable IP forwarding, and use two threads for poisoning and sniffing.

## 📚 Features
- Sends crafted ARP packets to poison target cache.
- Sniffs packets between victim and gateway.
- Proper cleanup and forwarding restore.

## ⚙️ Build & Run
```bash
make
sudo ./arp_poison <src_ip> <src_mac> <dst_ip> <dst_mac>
```

# Archinda

## 🕸️🦂 Spider & Scorpion

**Archinda** is a toolkit built as part of the 42 Cybersecurity Piscine.  
It includes two CLI tools focused on web and file metadata analysis:

- **Spider**: a recursive image web scraper.
- **Scorpion**: an EXIF metadata retriever for image files.

---

## 📦 Contents

### 🕷 Spider
A CLI tool that downloads images from a website, optionally recursing into subpages.

#### ✅ Features
- Recursive mode (`-r`)
- Recursion limit (`-l [N]`)
- Custom output directory (`-p [PATH]`)
- Default recursion depth: 5
- Default output folder: `./data/`

#### ⚙ Usage
```bash
make spider
./spider https://example.com
```
# Vaccine

## 💉 Educational SQL Injection Detector

**Vaccine** is a Python tool created for the 42 Cybersecurity Piscine.  
It scans a target URL with parameters to detect potential SQL injection (SQLi) vulnerabilities using:
- Union-based injection
- Boolean-based injection

It also attempts to identify the target database type from error messages.

---

## 🧰 Features
- Supports `GET` and `POST` methods.
- Detects:
  - Union-based SQLi
  - Boolean-based SQLi
- Attempts DB type detection (e.g., MySQL, SQLite).
- Saves scan results to a JSON archive file.

---

## ⚙️ Usage

Install dependencies:
```bash
pip install -r requirements.txt
```

# ft_onion

## 🧅 Upload HTML file over the Tor network

**ft_onion** is an educational project created as part of the 42 Cybersecurity Piscine.  
It demonstrates how to securely send (or "set") an HTML file to a hidden service using the Tor network.

---

## 📚 Features
- Connects to `.onion` hidden services via Tor.
- Sends an HTML file as content.
- Verifies upload response (or logs errors).

---

## ⚙️ Usage

Install requirements:
```bash
pip install -r requirements.txt
```
# ft_otp

## 🔐 Educational One-Time Password Tool

**ft_otp** is a project built for the 42 Cybersecurity Piscine.  
It demonstrates how to generate or validate One-Time Passwords (OTP) using standard algorithms like TOTP or HOTP.

---

## 📚 Features
- Generates OTP tokens from a shared secret.
- Optionally validates tokens entered by a user.
- Supports standard algorithms (e.g., TOTP: time-based).

---

## ⚙️ Usage

Build:
```bash
make
```

# ft_reverse

## 🔍 Educational Reverse Engineering Challenge

**ft_reverse** is part of the 42 Cybersecurity Piscine.  
The goal is to reverse engineer a provided binary, understand its logic, and either:
- Extract a hidden password or key
- Reproduce its behavior in C code

---

## 📚 What you'll find here
- Decompiled or reconstructed C source code from the binary.
- Analysis notes explaining the reverse engineering process.
- The extracted password or key needed to run or unlock the program.

---

## ⚙️ Tools & Techniques
- Static analysis: Ghidra, objdump, strings
- Dynamic analysis: gdb, ltrace/strace
- Understanding assembly and compiler patterns

---

## 📝 Usage
Build your reconstructed binary:
```bash
make
./ft_reverse
```

# irondome

## 🛡️ Educational Antivirus / Behavior-Based Detector

**irondome** is an educational cybersecurity tool built during the 42 Cybersecurity Piscine.  
It monitors system activity to detect suspicious behavior such as:
- Disk abuse (high number of file operations)
- Heavy cryptographic activity (possible ransomware encryption)

When suspicious activity is detected, it logs detailed alerts to a log file.

---

## 📚 Features
- Monitors file system and process activity in real time
- Detects:
  - Excessive file writes / deletions
  - Repeated cryptographic API calls or patterns
- Logs alerts with timestamps and activity details

---

## ⚙️ Usage

Build:
```bash
make
