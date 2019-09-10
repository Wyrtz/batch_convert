import FindWrongFormat
from pathlib import Path

wff = FindWrongFormat.wrong_format_finder(Path.cwd())
a,b = wff.find_wrong_format()

wff.print_wrong_format(padding_char="")