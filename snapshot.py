'''
Created on Jan 9, 2019
REQUIRES 32 Bit Version of WINDOWS
@author: BillyGates
'''
from pydbg import *
from pydbg.defines import *

import threading
import time
import sys

class snapshotter(object):
    
    def __init__(self, exe_path):
        
        self.exe_path   = exe_path
        self.pid        = None
        self.dbg        = None
        self.running    = True
        
        #Step 1: Start the debugger thread, and loop until
        # it set the PID of our target process
        # By using separate threads, we can enter snapshotting commands
        # without forcing the target application to pause while it waits for 
        # our input. 
        pydbg_thread = threading.Thread(target=self.start_debugger)
        pydbg_thread.setDaemon(0)
        pydbg_thread.start()
        
        while self.pid == None:
            time.sleep(1)
            
        #Step 2: We now have a PID and the target is running;
        # let's get a second thread running to do the snapshots
        monitor_thread = threading.Thread(target=self.monitor_debugger)
        monitor_thread.setDaemon(0)
        monitor_thread.start()
        
    #Step 3: 
    def monitor_debugger(self):
        
        while self.running == True:
            
            input = raw_input("Enther: 'snap' , 'restore' , or ' quit'")
            input = input.lower().strip()
            
            if input == "quit":
                print "[*] Exiting the snapshotter."
                self.running = False
                self.dbg.terminate_process()
            
            elif input == "snap":
                
                print "[*] Suspending all threads."
                self.dbg.suspend_all_threads()
                
                print "[*] Obtaining snapshot."
                self.dbg.process_snapshot()
                
                print "[*] Resuming operation."
                self.dbg.resume_all_threads()
                
            elif input == "restore":
                
                print "[*] Suspending all threads."
                self.dbg.suspend_all_threads()
                
                print "[*] Restoring snapshot."
                self.dbg.process_restore()
                
                print "[*] Resuming operation."
                self.dbg.resume_all_threads()
                
    #Step 4: Debugger thread returns a valid PID
    def start_debugger(self):
        
        self.dbg = pydbg()
        pid = self.dbg.load(self.exe_path)
        self.pid = self.dbg.pid
        
        self.dbg.run()
        
    #Step 5: set exe_path to the executable of your choice
    # we will use the calculator for the purpose of this example
exe_path = "C:\\WINDOWS\\System32\\calc.exe"
snapshotter(exe_path)
        
        