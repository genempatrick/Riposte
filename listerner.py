#!/usr/bin/python

import socket
import struct
import sys
import netifaces as ni
import argparse
import json
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--interface', type=str, help='Interface name')

args = parser.parse_args()

#get the interface's IP address
server_ip = ni.ifaddresses(args.interface)[ni.AF_INET][0]['addr']
port = 5355
multicast_group = '224.0.0.252'

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

def listener_llmnr():
    #set up the UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', port))
    #join the multicast group
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4s4s', group, socket.inet_aton(server_ip))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    #listen and receive traffic
    print(f"Listening on {server_ip}:{port}")
    while True:
        data, addr = sock.recvfrom(2048)
        now = datetime.now()
        address = addr[0] 
        header_removed = data[12:]
        hostname_parsed = parse_hostname(header_removed)

        print(now.strftime('%Y-%m-%d %H:%M:%S'), "[LLMNR]: Request from", address, "for hostname", hostname_parsed, "received.")

listener_llmnr()
