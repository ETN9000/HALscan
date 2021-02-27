import socket
from time import time, ctime


def startup():
    initTime = time()
    print(ctime(initTime))


startup()