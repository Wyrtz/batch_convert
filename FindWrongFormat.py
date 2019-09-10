import os
from pathlib import Path

class wrong_format_finder:
	
	def __init__(self, root, extention=None, ignore=None):
		if(not ignore):
			self.ignore = [".py", ".txt", ".png", ".jpg", ".mp4", ".srt", ".sub", ".rar", ".idx", ".zip", ".dvdrip-info", ".nfo", ".rtf",".bat", ".xlsx"]
		else:
			self.ignore = ignore
		self.p_root = Path(root)
		if(not self.p_root.exists()):
			 raise FileNotFoundError()
		if(extention):
			self.find = extention
		else:
			self.find = ""

	def find_wrong_format(self):
		unique = {}
		file_list = [i for i in self.p_root.glob("**/*.*")]
		relevant_file_list = []
		for file in file_list:
			if file.is_dir():
				continue
			file_name = file.suffix.lower()
			if (file_name not in self.ignore and (file_name == self.find or self.find == "")):
				relevant_file_list.append(file)
				try:
					unique[file_name] += 1
				except KeyError:
					unique[file_name] = 1
		
		self.relevant_file_list = relevant_file_list
		self.unique = unique

		return relevant_file_list, unique

	def print_wrong_format(self, fullPath=False ,padding_on=True, padding_length=15, padding_char = "*"):
		padding = padding_char*padding_length
		if(not self.relevant_file_list or not self.unique):
			print("No search performed")
			return
		if(padding_on):
			print(padding + "Undesired format{0}".format(": " + self.find) +padding)
		print("Total files in undesired format: " + str(len(self.relevant_file_list)))
		if (self.find == "") :
			print("Diffrent file extentions found: " + str(self.unique))
		for file in self.relevant_file_list:
			print(file.name) if not fullPath else print(str(file))