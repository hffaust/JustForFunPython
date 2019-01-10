'''
Created on Jan 8, 2019

@author: BillyGates

use: run buffer_overflow.py file, take note of its PID; it will 
pause until you are ready to let it run. Execute access_violation_handler.py (aka this file)
and enter in the PID of the test harness. Once the debugger has attached,
return to the console where the harness is running and hit any key to print out put.

You should have 4 sections of output:

1. tells you which instruction cause the access violation, as well as which module
that instruction lives in

2. the context dump of all the registers

3. a disassembly of the instructions before and after the faulting instructions

4. the list of structured exception handling (SEH) handlers that were registered at the
time of the crash
'''


from pydbg import *
from pydbg.defines import *

# Utility libraries included pydbg
import utils

# This is our access violation handler
def check_accessv(dbg):
    
    # We skip first-chance exceptions
    if dbg.dbg.u.Exception.dwFirstChance:
        return DBG_EXCEPTION_NOT_HANDLED
    
    crash_bin = utils.crash_binning.crash_binning()
    crash_bin.record_crash(dbg)
    print crash_bin.crash_synopsis()
    
    dbg.terminate_process()
    
    return DBG_EXCEPTION_NOT_HANDLED

pid = raw_input("Enter the Process ID: ")

dbg = pydbg()
dbg.attach(int(pid))
dbg.set_callback(EXCEPTION_ACCESS_VIOLATION, check_accessv)
dbg.run()