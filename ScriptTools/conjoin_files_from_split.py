import shutil
import os
import sys
from pathlib import Path


def album_song_printer(viable_path):
	proper_place_dirs = {}
	proper_place_files = []
	for dirName, subdirList, fileList in os.walk(str(viable_path)):
		# print('Found directory: %s' % dirName)
		
		proper_place_files = []
		for fname in fileList:
			# print('\t%s' % fname)
			proper_place_files.append(fname)
		proper_place_dirs[dirName] = proper_place_files

	# removes all blanks, aka entries made before the walk descends into an album
	copy_dict = proper_place_dirs.copy()
	for k in copy_dict.keys():
		if(copy_dict.get(k) == []):
			del proper_place_dirs[k]

	artist_album_to_songs_dict = {}
	for key in proper_place_dirs.keys():
		path = str(key).split("/")
		try:
			artist = path[-2]
		except IndexError as e:
			# print(e)
			pass
		try:
			album = path[-1]
		except IndexError as e:
			# print(e)
			pass
		try:
			print(key)
			print(str(artist)+"/"+str(album) + "\t" + str(proper_place_dirs.get(key)) + "\n")
			# dict of "<artist>/<allbum>" to ([song array], <path where it's located>)
			artist_album_to_songs_dict[str(artist)+"/"+str(album)] = (proper_place_dirs.get(key), key)
		except UnboundLocalError as e:
			# print(e)
			pass

	return(artist_album_to_songs_dict)


def compare(good_dir, bad_dir):
	file_rearrange = {}
	for key in bad_dir.keys():
		if(good_dir.get(key) != None):
			files_to_move, move_from_path = bad_dir.get(key)
			files_to_stay, move_to_path = good_dir.get(key)
			print(key, good_dir.get(key))
			print(key, bad_dir.get(key))
			print("\n")
			for item in bad_dir.get(key):
				if(item in good_dir.get(key)):
					print("HOLY FUCK WE HAVE A MATCH\n" + str(item) + " appears in both directories and should be resolved manually!\n")
					sys.exit(1)
					# this would show duplicate files
			file_rearrange[str(move_from_path)] = (files_to_move, move_to_path)
	return(file_rearrange)


def move_files_bitch(file_rearrange):
	counter = 0 
	for move_from_path in file_rearrange:
		# if(counter == 2):
		# 	sys.exit(0)
		files_to_move, move_to_path = file_rearrange.get(move_from_path)
		for file_name in files_to_move:
			complete_path = str(move_from_path)+"/"+str(file_name)
			print(complete_path)
			destination = shutil.move(str(complete_path), str(move_to_path)) 
		counter += 1
	print(str(counter) + " files moved BITCH!")


def main(argv):
	if(len(sys.argv) < 3):
		print("ERROR: INVALID NUMBER OF ARGS\nUSAGE: python3 conjoin_files.py <target dir> <dir to copy from>")
		sys.exit(1)
	target_path = sys.argv[1]  # good dir  aka  target dir
	source_path = sys.argv[2]  # bad dir   aka  dir to copy from
	print(target_path)
	print(source_path)

	good_dir = album_song_printer(target_path)
	print("\n\n\n")
	bad_dir = album_song_printer(source_path)
	# print(good_dir)   # test print
	print("\n\n\n")
	# print(bad_dir)    # test print

	file_rearrange = compare(good_dir, bad_dir)
	print("\n\n\n")
	print(file_rearrange)
	move_files_bitch(file_rearrange)
	# print(dir(os.path))
	# os.path.realpath will resolve symlinks AND return an absolute path from a relative path
	# print(os.path.realpath('.'))

	# os.path.abspath returns the absolute path, but does NOT resolve symlinks in its argument
	# print(os.path.abspath('.'))


if __name__ == "__main__":
	main(sys.argv[1:])
