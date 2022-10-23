# Import scapy
import scapy.all as scapy
# We need to create regular expressions to ensure that the input is correctly formatted.
import re

#logo
print ('''
   **********************************************************************
   *   ___         _     ___                                            *
   *   | _ \___ _ _| |_  / __| __ __ _ _ _  _ _  ___ _ _                *
   *   |  _/ _ \ '_|  _| \__ \/ _/ _` | ' \| ' \/ -_) '_|               *
   *   |_| \___/_|  \__| |___/\__\__,_|_||_|_||_\___|_|                 *
   *                                                                    *
   *    code from R3dHULK                                               *
   *    github page : https://github.com/R3DHULK                        *
   *                                                                    *
   **********************************************************************
   
   **********************************************************************
   *                                                                    *
   *  [!] Use This With Sudo Command or It'll Throw An Error            *
   *  [!] Works fine on only Linux Enviroment                           *
   *                                                                    *
   ********************************************************************** 
''')

# Regular Expression Pattern to recognise IPv4 addresses.
ip_add_range_pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]*$")

# Get the address range to ARP
while True:
    ip_add_range_entered = input("\nPlease enter the ip address and range that you want to send the ARP request to (ex 192.168.1.0/24): ")
    if ip_add_range_pattern.search(ip_add_range_entered):
        print(f"{ip_add_range_entered} is a valid ip address range")
        break


# Try ARPing the ip address range supplied by the user. 
# The arping() method in scapy creates a pakcet with an ARP message 
# and sends it to the broadcast mac address ff:ff:ff:ff:ff:ff.
# If a valid ip address range was supplied the program will return 
# the list of all results.
arp_result = scapy.arping(ip_add_range_entered)
input ("Enter To Exit")