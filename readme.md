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
