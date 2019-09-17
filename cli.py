import find_wrong_format
import format_wrong_formats
from printer import Printer
from pathlib import Path
import argparse

desc = "Description goes here"
parser = argparse.ArgumentParser(description=desc)
parser.add_argument("-t", "--target_file_extension", type=str, default=".mp4",
                    help="The format (extension) to format all videos into, eg .mp4. Default = .mp4")
parser.add_argument("-i", "--input_folder", type=str, default=Path.cwd(),
                    help="The path to the root folder of the file structure to traverse and convert to target format")
parser.add_argument("-d", "--delete_files", type=bool, default=False,
                    help="Should the input file be deleted after it is successfully converted ? Default = False")

args = parser.parse_args()

path = Path(args.input_folder)

if not path.exists():
    raise FileNotFoundError("The input-folder was not found: " + str(path))


def get_common_video_file_extensions() -> list:
    with open("common_video_file_extensions.txt", "r") as file:
        content = file.readlines()
    return [str(l).rstrip() for l in content]


com_ext = get_common_video_file_extensions()
target_extensions = args.target_file_extension

try:
    com_ext.remove(target_extensions)
except ValueError:
    error_message = (target_extensions + " is an unsupported format!"
                              " If you are sure ffmpeg supports this format,"
                              " add it to common_video_file_extensions.txt")
    raise ValueError(error_message)

printer = Printer()

fef = find_wrong_format.file_extension_finder(path, com_ext)
rel_files, unique = fef.find_files()
printer.print_wrong_format(rel_files, unique)

fwf = format_wrong_formats.file_converter()
fwf.add_observer(printer)

printer.print_section("Converting files")

failed_conversions = fwf.convert_files(rel_files, target_extensions, delete_files_when_done=args.delete_files)

if failed_conversions:
    printer.print_failed_conversions(failed_conversions, len(rel_files))

else:
    printer.print_section("Success")
    print("All files converted successfully!")


