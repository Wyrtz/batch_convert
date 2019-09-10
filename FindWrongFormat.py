import os
from pathlib import Path

root = input("Root path:")
find = input("extention:")

class wrong_format_finder:

	ignore = [".py", ".txt", ".png", ".jpg", ".mp4", ".srt", ".sub", ".rar", ".idx", ".zip", ".dvdrip-info", ".nfo", ".rtf",".bat", ".xlsx"]
	
	def __init__(root):
		p_root = Path(root)
		if(not p_root.exists()):
			 FileNotFoundError

	def find_wrong_format():
		unique = {}
		file_list = [i for i in file_folder.glob("**/*.*")]
		relevant_file_list = []
		for file in file_list:
			if file.is_dir():
				continue
			file_name = file.suffix.lower()
			if (file_name not in ignore and (file_name == find or find == "")):
				relevant_file_list.append(file)
				try:
					unique[file_name] += 1
				except KeyError:
					unique[file_name] = 1
					
		return relevant_file_list, unique

	def print_wrong_format():
		
	

			
print("*"*30)
print("Total files in undesired format: " + str(count))
if (find == "") :
	print("Diffrent file extentions found: " + str(unique))

input()
