import format_wrong_formats
import find_wrong_format
from pathlib import Path

padding = "*"*15
root = input("Root path:")
find = input("extention:")

ignore = [".py", ".txt", ".png", ".jpg", ".mp4", ".srt", 
".sub", ".rar", ".idx", ".zip", ".dvdrip-info", ".nfo", ".rtf",".bat", ".xlsx"]

#*** Main Logic
file_folder = Path(root)
format_finder = wrong_format_finder(root)
relevant_files, uniques = format_finder.find_wrong_format()