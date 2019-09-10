import os
from pathlib import Path

class wrong_format_finder:
	
	def __init__(self, root, extention=None, ignore=None):
		"""
		Args:
			root: root folder of search. All files and folders from this point will be a part of the search
			extention: if specified, the file extention to find eg. ".mkv"
			ignore: if specified, a list of file extentions to ignore
			ignore_extra: if specified, file extentions to be ignored on top of the default list
		"""
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
		"""Compile a list of files either matching self.find if set, else all files not in self.ignore starting from the root"""
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

	def print_wrong_format(self, fullPath=False, padding_on=True, padding_length=15, padding_char = "*"):
		"""
		Prints the result of the search
		Args:
			fullPath: print the full path of the files with wrong format. False = only file.name
			padding_on: whether or not any patting should be printed before the method lists the findings
			padding_length: size of padding before and after title
			padding_char: what char to pad with. Default "*"
		"""
		padding = padding_char*padding_length
		if(not self.relevant_file_list or not self.unique):
			print("No search performed")
			return
		if(padding_on):
			print(padding + "Undesired format{0}".format(" " + self.find) +padding)
		print("Total files in undesired format: " + str(len(self.relevant_file_list)))
		if (self.find == "") :
			print("Different file extentions found: " + str(self.unique))
		for file in self.relevant_file_list:
			print(file.name) if not fullPath else print(str(file))