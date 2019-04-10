'''
Created on Dec 18, 2018

@author: BillyGates
'''
from ctypes import *

msvcrt = cdll.msvcrt
message_string = "Hello world!\n"
msvcrt.printf("Testing: %s", message_string)

#if __name__ == '__main__':
#    pass