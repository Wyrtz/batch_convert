import os
from pathlib import Path

root = input("Root path:")
find = input("extention:")

ignore = [".py", ".txt", ".png", ".jpg", ".mp4", ".srt", 
".sub", ".rar", ".idx", ".zip", ".dvdrip-info", ".nfo", ".rtf",".bat", ".xlsx"]
	
unique = {}
file_folder = Path(root)

print("Found following files:")
print("*"*30)
count = 0
file_list = [i for i in file_folder.glob("**/*.*")]
for file in file_list:
	if file.is_dir():
		continue
	file_name = file.suffix.lower()
	if (file_name not in ignore and (file_name == find or find == "")):
		print(file)
		count += 1
		try:
			unique[file_name] += 1
		except KeyError:
			unique[file_name] = 1
		
print("*"*30)
print("Total files in undesired format: " + str(count))
if (find == "") :
	print("Diffrent file extentions found: " + str(unique))

input()
	