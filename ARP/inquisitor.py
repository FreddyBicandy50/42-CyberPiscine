from scapy.all import sniff, TCP, Raw

# List of FTP commands to look for
FTP_KEYWORDS = [b'USER', b'PASS', b'RETR', b'STOR', b'LIST', b'CWD', b'PWD', b'QUIT']

def process_packet(packet):
    if packet.haslayer(Raw) and packet.haslayer(TCP):
        payload = packet[Raw].load
        # Only show if payload starts with an FTP command
        for keyword in FTP_KEYWORDS:
            if payload.startswith(keyword):
                print(f"[FTP] {payload.decode(errors='ignore').strip()}")
                break

print("[*] Starting FTP sniffer on port 21...")
sniff(filter="tcp port 21", prn=process_packet, store=0)
