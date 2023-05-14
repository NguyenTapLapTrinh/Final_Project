import subprocess

def get_ip_address():
    # Execute the 'arp -a' command to get the ARP cache entries
    cmd = 'arp -a | findstr "40-1c-83-80-e1-ca" '
    returned_output = subprocess.check_output((cmd),shell=True,stderr=subprocess.STDOUT).decode()
    lines = returned_output.strip().split("\n")
    for line in lines:
        if "40-1c-83-80-e1-ca" in line.lower():
            parse=str(returned_output).split(' ',1)
            ip=parse[1].split(' ')
            return ip[1]
    return None

ip_address = get_ip_address()
if ip_address:
    print(ip_address)
else:
    print("MAC", )
    
import scapy

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1,
                              verbose=False)[0]

    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list 




