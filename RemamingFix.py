import os

for filename in os.listdir():
	index = int(str(filename).find("DVDRip"))
	if(index != -1):
		newName = str(filename)[0:index] + "mp4"
		print(filename + " -> \n" + newName, end="\n|\n")
		#os.rename(filename, newName)
input()
	