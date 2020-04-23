import random
def main():
	"""Main Program"""
	final = []
	size = input("Enter the size for the random salt:")
	for i in range(0, size):
		final.append(chr(random.randint(33, 126)))
	
	print(''.join(final))	
	return 0


if __name__ == "__main__":
	main()
