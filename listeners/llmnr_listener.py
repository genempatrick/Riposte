#!/usr/bin/python

import socket
import struct
import sys
import netifaces as ni
import argparse
from datetime import datetime

def parse_hostname(data):
    hostname = []
    i = 0
    while True:
        length = data[i]
        if length == 0:
            break
        i += 1
        label = data[i:i+length].decode('ascii')
        hostname.append(label)
        i += length
    return ".".join(hostname)

def listener_llmnr(server_ip):
    #set up the UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 5355))
    #join the multicast group
    group = socket.inet_aton('224.0.0.252')
    mreq = struct.pack('4s4s', group, socket.inet_aton(server_ip))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    #listen and receive traffic
    print(f"Listening on {server_ip}:5355")
    while True:
        data, addr = sock.recvfrom(2048)
        now = datetime.now()
        address = addr[0] 
        header_removed = data[12:]
        hostname_parsed = parse_hostname(header_removed)

        print(now.strftime('%Y-%m-%d %H:%M:%S'), "[LLMNR]: Request from", address, "for hostname", hostname_parsed, "received.")


