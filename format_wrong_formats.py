import os
import subprocess
from subprocess import CREATE_NEW_CONSOLE
from pathlib import Path


def convert_files(files_to_convert: list, fullPath=False, padding_on=True, padding_length=15, padding_char = "*"):
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
	ffmpeg_command = ".\\ffmpeg.exe -i \"{0}\" -codec copy \"{1}\"" #ToDo: make general
	nubmer_of_files_to_convert = len(files_to_convert)

	print()
	print(padding + "Converting files" + padding)
	print("\t-Starting to convert-")
	for index, file in enumerate(files_to_convert):
		i = file
		o = file.with_suffix(".mp4")
		completedProccess = subprocess.run(ffmpeg_command.format(i,o), creationflags=CREATE_NEW_CONSOLE)
		outcome = "Succes"
		if (completedProccess.returncode != 0):
			failed_conversions.append(file)
			outcome = "Failed"
		print("{0} converting file {1} of {2}: {3}".format(outcome, index, nubmer_of_files_to_convert, file.name))
		#delete -i

	print()
	if(failed_conversions):
		print(padding + "Failed files" + padding)
		print("{0} files out of {1} failed to convert!".format(len(failed_conversions), nubmer_of_files_to_convert))
		print("Unable to transcode the following files:")
		for file in failed_conversions:
			print("\t" + str(file))