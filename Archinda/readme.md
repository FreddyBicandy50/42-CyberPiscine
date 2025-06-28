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
