import find_wrong_format
import format_wrong_formats
from pathlib import Path

p = Path("\\\\WyrNAS\Multimedia\Videos\Code\Testfolder\Folder in folder")
wff = find_wrong_format.wrong_format_finder(p)

rel_files, uniques = wff.find_wrong_format()

wff.print_wrong_format()

fwf = format_wrong_formats.file_converter()
failed_conversions = fwf.convert_files(rel_files)

print()
if(failed_conversions):
    print(padding + "Failed files" + padding)
    print("{0} files out of {1} failed to convert!".format(len(failed_conversions), nubmer_of_files_to_convert))
    print("Unable to transcode the following files:")
    for file in failed_conversions:
        print("\t" + str(file))


