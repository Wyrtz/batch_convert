import subprocess
from observer_interface import Observer
from pathlib import Path


class VideoFileConverter:

	def __init__(self):
		self.observers = []

	def convert_files(self, files_to_convert: list,
					  target_extension: str,
					  ffmpeg_user_options: str,
					  delete_files_when_done=True,
					  output_folder = None):
		"""
		converts files in the list
			Args:
				files_to_convert: list containing the pathlib paths of the files to convert
				target_extension: the extension (eg .mp4) of the output files
				delete_files_when_done: delete the input file when a output file is generated successfully
				ffmpeg_user_options: the options to ffmpeg
		"""
		failed_conversions = []
		ffmpeg_user_options = ".\\ffmpeg.exe -i \"{0}\" " + ffmpeg_user_options + " \"{1}\""
		number_of_files_to_convert = len(files_to_convert)

		for index, file in enumerate(files_to_convert):
			i = Path(file)
			o = Path(file).with_suffix(target_extension)
			o = o.with_name(o.stem + "-tmp" + target_extension)
			if output_folder:
				o = Path(Path(output_folder) / i.name)
			#o = o.with_suffix(".tmp" + target_extension)
			completed_process = subprocess.run(ffmpeg_user_options.format(i, o))  # creationflags=CREATE_NEW_CONSOLE
			print("\r")
			outcome = "Success"
			if completed_process.returncode != 0:
				failed_conversions.append(file)
				outcome = "Failed"
			self.notify_all((outcome, index+1, number_of_files_to_convert, file.name))
			# print("{0} converting file {1} of {2}: {3}".format(outcome, index+1, number_of_files_to_convert, file.name))
			if completed_process.returncode == 0 and delete_files_when_done:
				file.unlink()
				o.rename(o.with_name(o.stem[:-4] + target_extension))

			elif completed_process.returncode != 0:
				if o.exists():
					o.unlink()

		return failed_conversions

	def add_observer(self, observer: Observer):
		self.observers.append(observer)

	def notify_all(self, message: tuple):
		for observer in self.observers:
			observer.update(message)
