import argparse
import netifaces as ni
from threading import Thread
from listeners.llmnr_listener import listener_llmnr
from listeners.mdns_listener import listener_mdns
from listeners.ntbs_listener import listener_ntbs
import time


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--interface', type=str, help='Interface name')

args = parser.parse_args()

#get the interface's IP address
server_ip = ni.ifaddresses(args.interface)[ni.AF_INET][0]['addr']

Thread(target=listener_llmnr, args=(server_ip,), daemon=True).start()
Thread(target=listener_mdns, args=(server_ip,), daemon=True).start()
Thread(target=listener_ntbs, args=(server_ip,), daemon=True).start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down.")