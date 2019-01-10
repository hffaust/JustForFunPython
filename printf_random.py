'''
Created on Jan 6, 2019

@author: BillyGates
'''
from pydbg import * 
from pydbg.defines import *

import struct
import random
#from my_debugger_defines import DBG_CONTINUE

# This is our user defined callback function 
def printf_randomizer(dbg):
    # Read in the value of the counter at ESP + 0x8 as a SWORD
    parameter_addr = dbg.context.Esp + 0x8
    counter = dbg.read_process_memory(parameter_addr, 4)
    # When we use read_process_memory, it returns a packed binary string.
    # We must first unpack it before we can use it further.
    
    counter = struct.unpack("L", counter)[0]
    print "Counter: %d" % int(counter)
    
    # Generate a random number and pack it into ninary format 
    # so that it is written correctly back into the process
    random_counter = random.randint(1, 100)
    random_counter = struct.pack("L", random_counter)[0]
    
    # Now swap in our random number and resume the process
    dbg.write_process_memory(parameter_addr, random_counter)
    return DBG_CONTINUE

# Instantiate the pydbg class
dbg = pydbg()  

# Now enter the PID of the printf_loop.py Process
pid = raw_input("Enter the printf_loop.py PID: ")

# Attatch the debugger to that Process
dbg.attach(int(pid))

#Set the breakpoint with the printf_randomizer Function
# defined as a callback
printf_address = dbg.func_resolve("msvcrt", "printf")
dbg.bp_set(printf_address, description="printf_address", handler=printf_randomizer)

# Resume the Process
dbg.run()