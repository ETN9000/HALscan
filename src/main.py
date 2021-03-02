from time import time, ctime, sleep
import os
import sys
import signal

from netifaces import *
import netifaces as netif
import ipaddress
import socket

import concurrent.futures
import logging

import argparse

from termcolor import colored, cprint

# Quick functions
def clr():
    os.system('cls' if os.name == 'nt' else 'clear')
def errprint(text):
    print(colored(text, 'red'))
def sprint(text):
    print(colored(text, 'green'))

hal = colored("[", attrs=['bold']) + colored("•", 'red') + colored("]", attrs=['bold'])

def exitHandler(signal, frame):
    clr()
    print("\n[!] Exitting now...")
    os._exit(1)
signal.signal(signal.SIGINT, exitHandler)

def parser():
    global args
    parser = argparse.ArgumentParser(description='Network scanning utility')
    parser.add_argument('--interface', dest='interface', type=str, nargs='?',
                        help='Interface to use (eg. wlan0, eth0)')
    parser.add_argument('--threads', dest='threads', type=int, nargs='?',
                        help='Amount of threads to use (default: 10)')
    args = parser.parse_args()

def interfacesetup():
    
    global macaddr
    global ipaddr
    global subnet 

    # Checks if there are interfaces, if there are any it will export the list to a var
    interfacelist = netif.interfaces()
    if not interfacelist:
        errprint("[✗] No interfaces available")
        exit()

    # Allows for user to select from a list of network interfaces and sets it as a variable
    global interface
    if args.interface:
        if any(word in args.interface for word in interfacelist):
            interface = args.interface
        else:
            errprint("[X] Invalid interface specified")
            exit()
    else:
        interface = input("[?] Enter the interface you would like to use? %s: " % interfacelist)
        if not any(word in interface for word in interfacelist):
            errprint("[X] Invalid option")
            exit()
        
    # Gets and prints interface attributes
    ## NOTE THIS DOES NOT WORK WITH MY eno1 INTERFACE FOR SOME REASON, FIX ASAP

    try:
        ipaddr = ''.join([i['addr'] for i in netif.ifaddresses(interface)[netif.AF_INET]])
        netmask = ''.join([i['netmask'] for i in netif.ifaddresses(interface)[netif.AF_INET]])
        subnet = ipaddress.ip_network(ipaddr + "/" + netmask, strict=False)
        print("[I] Interface Information")
        print(" └─[ Name       : %s" % interface)
        print(" └─[ IP Subnet  : %s" % str(subnet))
    except:
        errprint("[!] Interface has no valid IP address, cannot continue")
        exit()

    macaddr = ''.join([i['addr'] for i in netif.ifaddresses(interface)[netif.AF_LINK]])
    print(" └─[ MAC Address: %s" % macaddr)


def startup():
    def checkroot():
        if os.geteuid() != 0:
            errprint("[✗] User does not have root/sudo permissions")
            exit()
    def argcheck():
        global thread_count
        if args.threads:
            thread_count = args.threads
        else:
            thread_count = 10
    clr()
    print(hal + colored(" /// HALscan Version 1.0 ///", attrs=['bold']))
    print("HALscan initiated at: " + ctime(time()) + "\n")
    parser()
    checkroot()
    interfacesetup()

def portScan(target_ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)
        conn = s.connect_ex((target_ip, port))
        if conn == 0:
            sprint("[V] %s:%s open" % (target_ip, port))
            pass
        else:
            #errprint("[X] %s:%s" % (target_ip, port))
            pass



def main():
    print("[!] Startup complete!")
    #userconsent = input("[?] Would you like to begin scanning the subnet? [y/n]: ")
    #if userconsent != "y":
    #    errprint("[!] Shutting down")
    #    exit()

    def subnet_scanner():
        portlist = [22, 80]
        with concurrent.futures.ProcessPoolExecutor(max_workers=50) as executor:
            for ip in ipaddress.IPv4Network(subnet):
                for port in portlist:
                    executor.submit(portScan, str(ip), port)
    subnet_scanner()

startup()
main()