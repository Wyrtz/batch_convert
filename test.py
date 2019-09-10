import FindWrongFormat
from pathlib import Path

wff = FindWrongFormat.wrong_format_finder(Path.cwd(), extention=".py", ignore=[".hest"])
rel_files, uniques = wff.find_wrong_format()

wff.print_wrong_format()