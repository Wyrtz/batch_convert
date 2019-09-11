import os
from pathlib import Path

for filename in os.listdir(Path.cwd()):
	index = int(str(filename).find(".avi"))
	if(index != -1):
		newName = str(filename)[0:index] + ".mp4"
		print(filename + " -> \n" + newName, end="\n|\n")
		#os.rename(filename, newName)
input()
	