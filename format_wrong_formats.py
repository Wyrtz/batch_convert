import os
import subprocess
from subprocess import CREATE_NEW_CONSOLE
from pathlib import Path
from observer_interface import Observer


class file_converter:

	def __init__(self):
		self.observers: List[Observer] = []

	def add_observer(self, observer: Observer):
		self.observers.append(observer)
	
	def notify_all(self, message: String):
		for o in self.observers:
			o.update(message)

	def convert_files(self, files_to_convert: list, fullPath=False, padding_on=True, padding_length=15, padding_char = "*"):
		"""		
		converts files in the list
			Args:
				fullPath: print the full path of the files with wrong format. False = only file.name
				padding_on: whether or not any patting should be printed before the method lists the findings
				padding_length: size of padding before and after title
				padding_char: what char to pad with. Default "*"
		"""
		
		padding = padding_char*padding_length
		failed_conversions = []
		ffmpeg_IO = ".\\ffmpeg.exe -i \"{0}\" -codec copy \"{1}\"" #ToDo: make general
		ffmpeg_options = " -loglevel quiet -stats -y -benchmark_all"
		ffmpeg_command = ffmpeg_IO + ffmpeg_options
		nubmer_of_files_to_convert = len(files_to_convert)

		print()
		print(padding + "Converting files" + padding)
		print("\t-Starting to convert-")
		for index, file in enumerate(files_to_convert):
			i = file
			o = file.with_suffix(".mp4")
			#ToDo: new windows should not take focus
			completedProccess = subprocess.run(ffmpeg_command.format(i,o), capture_output=True) # creationflags=CREATE_NEW_CONSOLE
			print(completedProccess.stdout.decode("utf-8"))
			outcome = "Succes"
			if (completedProccess.returncode != 0):
				failed_conversions.append(file)
				outcome = "Failed"
			print("{0} converting file {1} of {2}: {3}".format(outcome, index+1, nubmer_of_files_to_convert, file.name))
			#delete -i

		return failed_conversions