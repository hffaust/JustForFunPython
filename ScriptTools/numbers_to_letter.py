import sys


def decodeString(coded_str, delim):
	# TODO: add modulo 26 line to decode 
	#   when alphabet loops. 0 = Z
	alpha_dict={
		1:'a',
		2:'b',
		3:'c',
		4:'d',
		5:'e',
		6:'f',
		7:'g',
		8:'h',
		9:'i',
		10:'j',
		11:'k',
		12:'l',
		13:'m',
		14:'n',
		15:'o',
		16:'p',
		17:'q',
		18:'r',
		19:'s',
		20:'t',
		21:'u',
		22:'v',
		23:'w',
		24:'x',
		25:'y',
		26:'z'
	}
	# first split on spaces, then on delim
	coded_str = coded_str.split(' ')
	print(coded_str)
	temp = []
	delim_word = ''
	decoded_str = []
	for word in coded_str:
		delim_word = ''
		if(delim in word):
			temp = word.split(delim)
			for letter in temp:
				alpha_letter = alpha_dict[int(letter)]
				delim_word += alpha_letter
			decoded_str.append(delim_word)
		else:
			decoded_str.append(alpha_dict[int(word)])
	print(decoded_str)


def main(argv):
	if(len(sys.argv) < 2):
		print("ERROR: INVALID NUMBER OF ARGUMENTS\nUSAGE: python3 numbers_to_letters.py \"<string to decode>\" ")
		sys.exit(1)

	coded_str = sys.argv[1]
	print("You entered:\n")
	print(coded_str)
	delim = input("What is the delimiter character?")
	decodeString(coded_str, delim)

if __name__ == '__main__':
	main(sys.argv[1:])
