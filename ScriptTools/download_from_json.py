'''
AUTHOR: H.Faust
DATE: 4.10.19
WRITTEN FOR PYTHON-V3 

Designed to be run as a standalone script for downloading multiple files from internet websites
  given that the url of the file location can be pulled from a json document, with the links to
  each file being contained in the 'download' key field of the json file.

*** If this script is not working for you the error most likely is in the *** 
     'parse_json_for_download' function. I oringally designed this function 
      to be used with a json format as follows:

    jsonroot:
     |
     |--->Child-1:
     |     |
     |     |----> { field-1: ... field-2: ... field-n: ... download: ... }
     |--->Child-2: 
     |     |
     |     |----> { ..... }
     |--->Child-n: 
     .
     .
     .  ect ...

'''

import sys
import json
import requests
import os 
import urllib.request
import urllib.error
#from time import time as timer


class JsonDownloader():
	def get_url(self, url):
		r = requests.get(url)
		print(str(r.status_code)+"\n")
		#print(str(r.headers['content-type']))  # test print 
		#print(str(r.encoding))  		# test print
		#print(str(r.text))			# test print
		json_return_temp = r.json()
		#print(str(json_return))		# test print
		return(json_return_temp)


	def parse_json_for_download(self, json_to_inspect):
		download_links = []
		json_holder = []
		keys = list(json_to_inspect.keys())
		for i in keys:
			json_holder.append(json_to_inspect.get(i))
		#print(json_holder)  	# test print
		for j in json_holder:
			for x in range(0, len(j)):
				print(str(j[x]) + "\n")
				if(j[x].get('download') == '#'):
					continue
				else:
					download_links.append(j[x].get('download'))
		print("\n")
		#print(download_links)   # test print
		return(download_links)

		
	def download_files(self, download_links, save_path, number_of_files):
		print("\ndownload_files(self, download_links, save_path) called!\n")    	 # test print
		num_of_files = len(download_links)
		if(num_of_files < 1 or num_of_files == None or save_path == None):
			print("ERROR: NO VALID DOWNLOAD LINKS OR FILEPATH\n...NOW EXITING...\n")
			sys.exit(1)
		for i in range(0, number_of_files): 						 # number_of_files -->  entered by user in driver
			try:
				file_url = download_links[i]
				this_file = urllib.request.urlopen(file_url)
				print("Downloading " + str(file_url))				 # test print 
				file_path = os.path.join(save_path, os.path.basename(file_url))  # contructs path to save downloads to
				with open(file_path, "wb") as local_file:			 # wb stands for 'write binary' file
					local_file.write(this_file.read())
					local_file.close() 					 # closes file writer
			# handle errors
			except urllib.error.HTTPError as e:
				print("\nHTTP Error: " + str(e.code) + " " + str(file_url)) 
			except urllib.request.URLError as e:
				print("\nURL Error: " + str(e.reason) + " " + str(file_url))
		print("\nDONE!")


def main(argv):
	#print(os.name)  					# test print
	if(len(sys.argv) < 3):
		print("ERROR: INVALID NUMBER OF ARGS\nUSAGE: python3 <filename.py> <url> <path to save files>\n")
		sys.exit(1)
	url = sys.argv[1]
	save_path = sys.argv[2]
	if(os.path.isdir(save_path)):
		print("save_path " + str(save_path) + " exists!\n")
	else:
		print("ERROR: INVALID PATH ---> "+ str(save_path) + "\n...NOW EXITING...\n")
		sys.exit(1)
	print("\nRetrieving URL: " + str(url) +"\n") 		# test print
	json_to_inspect = JsonDownloader().get_url(url)
	download_links = JsonDownloader().parse_json_for_download(json_to_inspect)
	number_of_files = 0
	for index in range(0,len(download_links)):
		print("Index #: " + str(index) + " = " + str(download_links[index]))
	input_loop = True
	while(input_loop):
		num_files = input("How many files would you like to try and download?\nPress 'a' for all\n")
		if(num_files == "a"):
			number_of_files = len(download_links)
			input_loop = False
		elif(num_files.isdigit() == True):
			number_of_files = int(num_files)
			input_loop = False
		else:
			print("ERROR: Invalid Input!... Try Again...") 
	JsonDownloader().download_files(download_links, save_path, number_of_files)
	print("\nProgram Finished!")

if __name__ == "__main__":
	main(sys.argv[1:])
