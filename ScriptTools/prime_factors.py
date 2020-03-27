import sys
import math
# A function to print all prime factors of  
# a given number n 
def primeFactors(n):   
    # Print the number of two's that divide n 
    while n % 2 == 0: 
        #print 2,
        print 2 
        n = n / 2
          
    # n must be odd at this point 
    # so a skip of 2 ( i = i + 2) can be used 
    for i in range(3,int(math.sqrt(n))+1,2): 
          
        # while i divides n , print i ad divide n 
        while n % i== 0: 
            #print i, 
            print i
            n = n / i 
              
    # Condition if n is a prime 
    # number greater than 2 
    if n > 2: 
        print n 



def main(argv):
    if(len(sys.argv) < 2):
        print "ERROR: INVALID NUMBER OF ARGUMENTS\nUSAGE: python prime_factors.py <number to factor>"
        sys.exit(1)
    num_to_factor = sys.argv[1]
    primeFactors(int(num_to_factor))
if __name__ == "__main__":
    main(sys.argv[1:])
