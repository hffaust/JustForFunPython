#!/usr/bin/python
'''
	This is ascii <-> shellcode encode / decoder tool
	This was written for educational purpose only. or fucking messing around...
	i.e how to use encode mode :
		--------------------------------------------------------------
		<username>:~/shellcode$ ./shellcodeencdec.py
		shellcode hex encode decoder
		what do you want to do ? encode / decode
		=> encode
		Please input data : /bin
		shellcode => \x2f\x62\x69\x6e
		<username>::~/shellcode$
		--------------------------------------------------------------
	i.e how to use decode mode :
		"\x68\x2f\x2f\x73\x68"  // push   $0x68732f2f
		"\x68\x2f\x62\x69\x6e"  // push   $0x6e69622f
		we know 'x68' is push, so drop it...
		"\x2f\x2f\x73\x68"     $0x68732f2f
		"\x2f\x62\x69\x6e"     $0x6e69622f
		--------------------------------------------------------------
		<username>:~/shellcode$ ./shellcodeencdec.py
		shellcode hex encode decoder
		what do you want to do ? encode / decode
		=> decode
		Please input data : \x2f\x2f\x73\x68
		hex       =>  2f2f7368
		plaintext => //sh
		<username>:~/shellcode$ ./shellcodeencdec.py
		shellcode hex encode decoder
		what do you want to do ? encode / decode
		=> decode
		Please input data : \x2f\x62\x69\x6e
		hex       =>  2f62696e
		plaintext => /bin
		--------------------------------------------------------------
		and we got that is "/bin//sh"
		
	warning ! this is not disassemble tool !
'''
import binascii, sys, time

RED = '\033[31m'
WHITE = '\033[37m'
RESET = '\033[0;0m'

def main():
	print "shellcode hex encode decoder"
	print "what do you want to do ? %sencode%s / %sdecode%s" % (RED, RESET, WHITE, RESET)
	q = raw_input("=> ")

	if q == "encode": 
		inputtype = raw_input("Please input data : ")
		print "shellcode => ",
		for encoded in inputtype:
			print "\b\\x"+encoded.encode("hex"),
			sys.stdout.flush()
			time.sleep(0.5)
			print RESET

	elif q == "decode":
		inputtype = raw_input("Please input data : ")
		cleaninput = inputtype.replace("\\x","")
		print "hex       => ",cleaninput
		print "plaintext => ",
		print "\b"+cleaninput.decode("hex")

	else:
		print "wrong answer ! your choice is %sencode%s or %sdecode%s" % (RED, RESET, WHITE, RESET)
		sys.exit(1)		

if __name__ == '__main__':
	main()

