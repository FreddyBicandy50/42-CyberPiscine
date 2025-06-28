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
