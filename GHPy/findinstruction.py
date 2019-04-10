'''
Created on Jan 10, 2019

@author: BillyGates
'''
import sys
#sys.path.append('C:/Python27_1')
#sys.path.append('C:/Python27_1/Lib') 
sys.path.append('C:/Program Files/Immunity Inc/Immunity Debugger')
sys.path.append('C:/Program Files/Immunity Inc/Immunity Debugger/Libs')

from immlib import *

def main(args):
    
    imm = Debugger()
    search_code = " ".join(args)
    
    # First, assemble the instructions we are searching for
    search_bytes = imm.Assemble(search_code)
    # Use the Search() method to search all of the memory
    # in the loaded binary for the instruction bytes
    search_results = imm.Search(search_bytes)
    
    for hit in search_results:
        # Retrieve the memory page where the hit exists
        # and make sure it's executable
        code_page = imm.getMemoryPagebyAddress(hit)
        access = code_page.getAccess(human=True)
        
        if "execute" in access.lower():
            imm.log("[*] Found: %s (0x%08x)" % (search_code, hit), address=hit)
    
    return "[*] Finished searching for instructions, check the Log window."