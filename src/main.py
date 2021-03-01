import socket
from time import time, ctime, sleep
import os
import sys
from netifaces import *
import netifaces as netif
import ipaddress

import threading
from queue import Queue

from termcolor import colored, cprint
import signal

# Quick functions
def clr():
    os.system('cls' if os.name == 'nt' else 'clear')
def errprint(text):
    print(colored(text, 'red'))
def sprint(text):
    print(colored(text, 'green'))
hal = colored("[", attrs=['bold']) + colored("•", 'red') + colored("]", attrs=['bold'])


def exitHandler(signal, frame):
    print("\n[!] Exitting now...")
    os._exit(1)
signal.signal(signal.SIGINT, exitHandler)

def startup():
    def checkroot():
        if os.geteuid() != 0:
            errprint("[✗] User does not have root/sudo permissions")
            exit()

    def interfacesetup():
        # Checks if there are interfaces, if there are any it will export the list to a var
        interfacelist = netif.interfaces()
        if not interfacelist:
            errprint("[✗] No interfaces available")
            exit()

        # Allows for user to select from a list of network interfaces and sets it as a variable
        global interface
        interface = input("[?] Enter the interface you would like to use? %s: " % interfacelist)
        if not any(word in interface for word in interfacelist):
            errprint("[✗] Invalid option")
            exit()
        
        # Gets and prints interface attributes
        ## NOTE THIS DOES NOT WORK WITH MY eno1 INTERFACE FOR SOME REASON, FIX ASAP

        global macaddr
        global ipaddr
        global subnet 
        try:
            ipaddr = ''.join([i['addr'] for i in netif.ifaddresses(interface)[netif.AF_INET]])
            netmask = ''.join([i['netmask'] for i in netif.ifaddresses(interface)[netif.AF_INET]])
            subnet = ipaddress.ip_network(ipaddr + "/" + netmask, strict=False)
            print("[I] Interface Information")
            print(" └─[ IP Subnet  : " + str(subnet))
        except:
            errprint("[!] Interface has no valid IP address, cannot continue")
            exit()

        macaddr = ''.join([i['addr'] for i in netif.ifaddresses(interface)[netif.AF_LINK]])
        print(" └─[ MAC Address: " + macaddr)
    
    
    clr()
    print(hal + colored(" /// HALscan Version 1.0 ///", attrs=['bold']))
    print("HALscan initiated at: " + ctime(initTime) + "\n")
    print("[+] Performing startup checks")
    checkroot()
    interfacesetup()


def portCheck(target_ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        conn = s.connect_ex((target_ip, port))
        if conn == 0:
            sprint("[V] %s:%s open" % (target_ip, port))
        else:
            errprint("[X] %s:%s" % (target_ip, port))

def main():
    print("[!] Startup complete!")
    global initTime
    initTime = time()
    #userconsent = input("[?] Would you like to begin scanning the subnet? [y/n]: ")
    #if userconsent != "y":
    #    errprint("[!] Shutting down")
    #    exit()

    portlist = [22, 80, 433]

    for ip in ipaddress.IPv4Network(subnet):
        for port in portlist:
            portCheck(str(ip), port)
    else:
        print("[!] Scan complete!")


startup()
main()