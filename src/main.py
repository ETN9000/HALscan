import socket
from time import time, ctime
import os
from netifaces import AF_INET, AF_INET6, AF_LINK, AF_PACKET, AF_BRIDGE
import netifaces as netif


def startup():
    def checkroot():
        if os.geteuid() != 0:
            print("[✗] User does not have root/sudo permissions")
            exit()
        else:
            print("[✓] User has root/sudo permissions")
    def interfacechk():
        interfaces = netif.interfaces()
        if not interfaces:
            print("[✗] No interfaces available")
        else:
            print("[✓] Available interfaces:", *interfaces, sep=" ")

    checkroot()
    interfacechk()

initTime = time()
print("[+] HALscan initiated at: " + ctime(initTime))
print("[+] Performing startup checks")
startup()