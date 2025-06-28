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
