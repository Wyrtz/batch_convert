import os
import subprocess
from subprocess import CREATE_NEW_CONSOLE
from pathlib import Path

padding = "*"*15
root = input("Root path:")
find = input("extention:")

ignore = [".py", ".txt", ".png", ".jpg", ".mp4", ".srt", 
".sub", ".rar", ".idx", ".zip", ".dvdrip-info", ".nfo", ".rtf",".bat", ".xlsx"]

#*** Main Logic
file_folder = Path(root)



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


print(padding + "Files in wrong format" + padding)
for path in relevant_file_list:
	print(path)
print("")
print("Total files in undesired format: " + str(len(relevant_file_list)))
if (find == "") :
	print("Diffrent file extentions found: " + str(unique))

failed_conversions = []
ffmpeg_command = ".\\ffmpeg.exe -i \"{0}\" -codec copy \"{1}\""
numb_of_relevant_files = len(relevant_file_list)

print()
print(padding + "Converting files" + padding)
print("\t-Starting to convert-")
for index, file in enumerate(relevant_file_list):
	i = file
	o = file.with_suffix(".mp4")
	completedProccess = subprocess.run(ffmpeg_command.format(i,o), creationflags=CREATE_NEW_CONSOLE)
	outcome = "Succes"
	if (completedProccess.returncode != 0):
		failed_conversions.append(file)
		outcome = "Failed"
	print("{0} converting file {1} of {2}: {3}".format(outcome, index, numb_of_relevant_files, file.name))
	#delete -i

print()
if(failed_conversions):
	print(padding + "Failed files" + padding)
	print("{0} files out of {1} failed to convert!".format(len(failed_conversions), numb_of_relevant_files))
	print("Unable to transcode the following files:")
	for file in failed_conversions:
		print("\t" + str(file))