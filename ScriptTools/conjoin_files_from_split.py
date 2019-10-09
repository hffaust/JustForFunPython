import shutil
import os
from pathlib import Path


def album_song_printer(viable_path):
	proper_place_dirs = {}
	proper_place_files = []
	for dirName, subdirList, fileList in os.walk(viable_path):
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
			artist = path[8]
		except IndexError as e:
			# print(e)
			pass
		try:
			album = path[9]
		except IndexError as e:
			# print(e)
			pass
		try:
			print(str(artist)+"/"+str(album) + "\t" + str(proper_place_dirs.get(key)) + "\n")
			artist_album_to_songs_dict[str(artist)+"/"+str(album)] = proper_place_dirs.get(key)
		except UnboundLocalError as e:
			# print(e)
			pass

	return(artist_album_to_songs_dict)


def compare(good_dir, bad_dir):
	for key in bad_dir.keys():
		if(good_dir.get(key) != None):
			print(key, good_dir.get(key))
			print(key, bad_dir.get(key))
			print("\n")
			for item in bad_dir.get(key):
				if(item in good_dir.get(key)):
					print("HOLY FUCK WE HAVE A MATCH\n" + str(item) + " appears in both directories and should be resolved manually!\n")
					# this would show duplicate files


def main():
	directory_1 = '/Users/hffaust/Nextcloud/Music/iTunes'

	directory_2 = '/Users/hffaust/Nextcloud/Music/iTunes/Music'

	directory_3 = "../../../../Nextcloud/Music/Music/."

	directory_4 = "../../../../Nextcloud/Music/iTunes/."

	good_dir = album_song_printer(directory_3)
	print("\n\n\n")
	bad_dir = album_song_printer(directory_4)

	print(good_dir)
	print("\n\n\n")
	print(bad_dir)

	compare(good_dir, bad_dir)


if __name__ == "__main__":
	main()
