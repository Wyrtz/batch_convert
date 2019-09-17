import subprocess
from observer_interface import Observer


class file_converter:

	def __init__(self):
		self.observers = []

	def convert_files(self, files_to_convert: list, target_extensions: str, delete_files_when_done=True):
		"""
		converts files in the list
			Args:
				files_to_convert: list containing the pathlib paths of the files to convert
				target_extensions: the extension (eg .mp4) of the output files
				delete_files_when_done: delete the input file when a output file is generated successfully
		"""
		failed_conversions = []
		ffmpeg_IO = ".\\ffmpeg.exe -i \"{0}\" -codec copy \"{1}\"" # ToDo: make general
		ffmpeg_options = " -loglevel quiet -stats -y -benchmark_all"
		ffmpeg_command = ffmpeg_IO + ffmpeg_options
		number_of_files_to_convert = len(files_to_convert)

		for index, file in enumerate(files_to_convert):
			i = file
			o = file.with_suffix(target_extensions)
			completed_process = subprocess.run(ffmpeg_command.format(i, o))  # creationflags=CREATE_NEW_CONSOLE
			outcome = "Success"
			if completed_process.returncode != 0:
				failed_conversions.append(file)
				outcome = "Failed"
			self.notify_all((outcome, index+1, number_of_files_to_convert, file.name))
			# print("{0} converting file {1} of {2}: {3}".format(outcome, index+1, number_of_files_to_convert, file.name))
			# delete -i
			#if completed_process.returncode == 0 and delete_files_when_done:
			#	Path(file).unlink()

		return failed_conversions

	def add_observer(self, observer: Observer):
		self.observers.append(observer)

	def notify_all(self, message: tuple):
		for observer in self.observers:
			observer.update(message)
