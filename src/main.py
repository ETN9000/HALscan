import socket
from time import time, ctime, sleep
import os
from netifaces import AF_INET, AF_INET6, AF_LINK, AF_PACKET, AF_BRIDGE
import netifaces as netif
import logging
from termcolor import colored, cprint
from alive_progress import alive_bar



# Global variables
initTime = time()

# Quick functions
def clr():
    os.system('cls' if os.name == 'nt' else 'clear')
def errprint(text):
    print(colored(text, 'red'))
hal = colored("[", attrs=['bold']) + colored("•", 'red') + colored("]", attrs=['bold'])

def startup():
    def checkroot():
        if os.geteuid() != 0:
            errprint("[✗] User does not have root/sudo permissions")
            exit()
        #else:
        #    print("[✓] User has root/sudo permissions")
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
        macaddr = ''.join([i['addr'] for i in netif.ifaddresses(interface)[netif.AF_LINK]])
        ipaddr = ''.join([i['addr'] for i in netif.ifaddresses(interface)[netif.AF_INET]])
        print("[I] Interface Information")
        print(" └─[ MAC Address: " + macaddr)
        print(" └─[ IP Address : " + ipaddr)

    clr()
    print(hal + colored(" /// HALscan Version 1.0 ///", attrs=['bold']))
    print("HALscan initiated at: " + ctime(initTime) + "\n")
    print("[+] Performing startup checks")
    checkroot()
    interfacesetup()


def main():
    print("[!] Startup complete!")
    print("[!] Running a dummy task!")
    
    def compute():
        for i in range(1000):
            sleep(.05)  # process items
            yield  # insert this and you're done!

    with alive_bar(1000) as bar:
        for i in compute():
            bar()
    





startup()
main()