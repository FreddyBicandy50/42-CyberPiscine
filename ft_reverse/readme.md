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
