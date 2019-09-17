import find_wrong_format
import format_wrong_formats
from printer import Printer
from pathlib import Path
import argparse


class CLI:

    def __init__(self):
        self.args = self.build_parser()
        self.com_vid_fil_ext = self.get_common_video_file_extensions()
        self.path = Path(self.args.input_folder)
        if not self.path.exists():
            raise FileNotFoundError("The input-folder was not found: " + str(self.path))
        self.target_extension = self.args.target_file_extension
        self.ext_to_look_for = self.get_list_of_extensions_to_look_for(self.com_vid_fil_ext, self.target_extension)
        self.printer = Printer()
        rel_files, unique = self.find_wrong_formats(self.path, self.ext_to_look_for)
        if not rel_files or self.args.just_scan:    # No files found, or user asks not to convert
            return
        self.format(rel_files, self.target_extension, self.args.delete_files)

    def get_common_video_file_extensions(self) -> list:
        with open("common_video_file_extensions.txt", "r") as file:
            content = file.readlines()
        return [str(l).rstrip() for l in content]

    def build_parser(self):
        desc = "Description goes here"
        parser = argparse.ArgumentParser(description=desc)
        parser.add_argument("-t", "--target_file_extension", type=str, default=".mp4",
                            help="The format (extension) to format all videos into, eg .mp4. Default = .mp4")
        parser.add_argument("-i", "--input_folder", type=str, default=Path.cwd(),
                            help="The path to the root folder of the file structure to traverse and convert to target format")
        parser.add_argument("-d", "--delete_files", type=bool, default=False,
                            help="Should the input file be deleted after it is successfully converted ? Default = False")
        parser.add_argument("-s", "--just_scan", type=bool, default=False,
                            help="Don't convert anything yet, just print the found files")

        return parser.parse_args()

    def get_list_of_extensions_to_look_for(self, lst: list, target_extension: str) -> list:
        try:
            lst.remove(target_extension)
        except ValueError:
            error_message = (target_extension + " is an unsupported format!"
                                                 " If you are sure ffmpeg supports this format,"
                                                 " add it to common_video_file_extensions.txt")
            raise ValueError(error_message)
        return lst

    def find_wrong_formats(self, path: Path, ext_to_look_for: list) -> (list, list):
        fef = find_wrong_format.FileExtensionFinder(path, ext_to_look_for)
        rel_files, unique = fef.find_files()
        self.printer.print_wrong_format(rel_files, unique)
        return rel_files, unique

    def format(self, rel_files: list, target_extensions: str, delete_files_when_done:bool):
        fwf = format_wrong_formats.VideoFileConverter()
        fwf.add_observer(self.printer)
        self.printer.print_section("Converting files")
        failed_conversions = fwf.convert_files(rel_files,
                                               target_extensions,
                                               delete_files_when_done=delete_files_when_done)

        if failed_conversions:
            self.printer.print_failed_conversions(failed_conversions, len(rel_files))

        else:
            self.printer.print_section("Success")
            print("All files converted successfully!")


if __name__ == "__main__":
    CLI()
else:
    print("Don't call this class from other Python modules!")
