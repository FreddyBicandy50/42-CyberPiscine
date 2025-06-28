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
