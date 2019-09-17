from pathlib import Path

class file_extension_finder:
	
	def __init__(self, root, extensions_to_find: list):
		"""
		Args:
			root: root folder of search. All files and folders from this point will be a part of the search
			extensions_to_find: A list of file extensions to look for. If no list is provided, all files will be returned
		"""
		self.p_root = Path(root)
		if not self.p_root.exists():
			raise FileNotFoundError()
		self.ext_to_find = extensions_to_find

	def find_files(self):
		"""
		Compile a list of all files path with extension as provided in the constructor
		"""
		unique = {}
		file_list = [i for i in self.p_root.glob("**/*.*")]
		relevant_file_list = []
		for file in file_list:
			if file.is_dir():
				continue
			file_name = file.suffix.lower()
			if file_name in self.ext_to_find or not self.ext_to_find:
				relevant_file_list.append(file)
				try:
					unique[file_name] += 1
				except KeyError:
					unique[file_name] = 1

		return relevant_file_list, unique
