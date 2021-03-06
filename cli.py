import find_wrong_format
import format_wrong_formats
from printer import Printer
from pathlib import Path
import argparse


class CLI:
    # ToDo: Make work on Linux too
    # ToDo: Make nice printer:
        # Delete the -stat after a file is completed
        # Show the name of the file being converted

    quiet_log = "-loglevel quiet -stats -y"
    codex_copy = "-c copy"

    def __init__(self):
        self.args = self.build_parser()
        self.ext_to_look_for = self.get_common_video_file_extensions()
        self.path = Path(self.args.input_folder)
        if not self.path.exists():
            raise FileNotFoundError("The input-folder was not found: " + str(self.path))
        self.target_extension = self.args.target_file_extension
        if self.args.codex_copy:
            self.ext_to_look_for = self.get_list_of_extensions_to_look_for(self.ext_to_look_for, self.target_extension)
        self.printer = Printer()
        rel_files, unique = self.find_wrong_formats(self.path, self.ext_to_look_for)
        if not rel_files or self.args.just_scan:    # No files found, or user asks not to convert
            return
        if self.args.codex_copy:
            self.args.ffmpeg_arguments = self.codex_copy + " " + self.args.ffmpeg_arguments
        failed_conversions = self.format(rel_files,
                                        self.target_extension,
                                        self.args.dont_delete_files,
                                        self.args.ffmpeg_arguments,
                                        self.args.output_folder)
        if failed_conversions:
            self.printer.print_failed_conversions(failed_conversions, len(rel_files))
            self.printer.print_section("Retry failed conversions")
            print("Do you want to re-encode the failed files ? (much slower process)")
            answer = input("y/n: ")
            if answer.lower() == "y":
                new_failed_conversions = self.format(failed_conversions,
                                         self.target_extension,
                                         self.args.dont_delete_files,
                                         self.quiet_log,
                                         self.args.output_folder)
                if new_failed_conversions:
                    self.printer.print_failed_conversions(new_failed_conversions, len(failed_conversions))

        else:
            self.printer.print_section("Success")
            print("All files converted successfully!")

    def get_common_video_file_extensions(self) -> list:
        with open("common_video_file_extensions.txt", "r") as file:
            content = file.readlines()
        return [str(l).rstrip().lower() for l in content]

    def build_parser(self):
        desc = "Command line interface for batch converting video files into a given file format. " \
               "Uses ffmpeg as converter. Default will use ffmpeg without arguments, but your own " \
               "conversion settings can be set with the -a argument. Will by default skip files in " \
               "target format that already exist eg. video.mkv will not be transcoded to" \
               "video.mp4 if this file already exists"

        parser = argparse.ArgumentParser(description=desc)
        parser.add_argument("-t", "--target_file_extension", type=str, default=".mp4",
                            help="The format (extension) to format all videos into, eg .mp4. Default = .mp4")
        parser.add_argument("-i", "--input_folder", type=str, default=Path.cwd(),
                            help="The path to the root folder of the file structure to traverse and convert to target format")
        parser.add_argument("-d", "--dont_delete_files", default=True, action="store_false",
                            help="Delete the input file after it is successfully converted. Default = True")
        parser.add_argument("-s", "--just_scan", default=False, action="store_true",
                            help="Don't convert anything yet, just print the found files")
        parser.add_argument("-f", "--ffmpeg_arguments", type=str,
                            default="-loglevel quiet -stats -y",
                            help="Arguments to ffmpeg. "
                                 "If provided, will have the structure "
                                 "\"ffmpeg.exe -i [input_file] [your parameters] [output_file] "
                                 "Default is \".\\ffmpeg.exe -i [input_file] [output_file] -loglevel quiet -stats -y\" ")
        parser.add_argument("-c", "--codex_copy", default=False, action="store_true",
                            help="Keep the codex and quality, just change file format")
        parser.add_argument("-o", "--output_folder", type=str, default=None,
                            help="Folder to place the converted files in. Default = same path as before converting")
        #ToDo:
        # parser.add_argument("-o", "--output_folder", type=str,
        #                    help="Put all transcoded files at this path (folder)")

        return parser.parse_args()

    def get_list_of_extensions_to_look_for(self, lst: list, target_extension: str) -> list:
        target_extension = target_extension.lower()
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

    def format(self, rel_files: list, target_extensions: str,
               delete_files_when_done: bool, ffmpeg_arguments: str, output_folder=None) -> list:
        fwf = format_wrong_formats.VideoFileConverter()
        fwf.add_observer(self.printer)
        self.printer.print_section("Converting files")
        failed_conversions = fwf.convert_files(rel_files,
                                               target_extensions,
                                               ffmpeg_arguments,
                                               delete_files_when_done=delete_files_when_done,
                                               output_folder=output_folder)
        return failed_conversions


if __name__ == "__main__":
    CLI()
else:
    print("Don't call this class from other Python modules!")
