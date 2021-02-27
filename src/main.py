import socket
from time import time, ctime
import os
from netifaces import AF_INET, AF_INET6, AF_LINK, AF_PACKET, AF_BRIDGE
import netifaces as netif
import logging

# Global variables
initTime = time()

def startup():
    def checkroot():
        if os.geteuid() != 0:
            print("[✗] User does not have root/sudo permissions")
            exit()
        else:
            print("[✓] User has root/sudo permissions")
    def interfacechk():
        interfacelist = netif.interfaces()
        if not interfacelist:
            print("[✗] No interfaces available")
            exit()
        else:
            print("[✓] Available interfaces:", *interfacelist, sep=" ")

    print("[+] HALscan initiated at: " + ctime(initTime))
    print("[+] Performing startup checks")

    checkroot()
    interfacechk()




def netmapper():
    print("[I] Beginning Network Mapping on")








def main():
    print("\n" + "/// HALscan Version 1.0 ///\n")

    interface = input("Enter the interface you would like to use? %s: " % netif.interfaces() )
    if any(word in interface for word in netif.interfaces()):
        print("[✓] Valid choice")
    else:
        print("Invalid option")





startup()
main()