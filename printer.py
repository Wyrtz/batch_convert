from observer_interface import Observer


class Printer(Observer):

    def __init__(self, padding_char="-", padding_length=15):
        self.padding_char = padding_char
        self.padding_length = padding_length
        self.padding = self.padding_char*self.padding_length
    
    def update(self, update: tuple):
        print("{} converting file {} of {}: {}".format(*update))

    def print_section(self, message: str, spacing=1):
        for i in range(spacing):
            print()
        print(self.padding + message + self.padding)

    def print_wrong_format(self, file_list: list, unique_file_extension: list, full_path=False):
        """
        Prints the result of the search
        Args:
            file_list: the list of files to print
            unique_file_extension: dictionary of key:filetype (string) value: amount found (int)
                                   as created by find_wrong_format
            full_path: print the file.name or the entire path

        """
        self.print_section("Undesired format")
        for file in file_list:
            print(file.name) if not full_path else print(str(file))
        print()
        print("Total files in undesired format: " + str(len(file_list)))
        print("Different file extensions found: " + str(unique_file_extension))

    def print_failed_conversions(self, failed_conversions, number_of_files):
        self.print_section("Failed files")
        print("{0} files out of {1} failed to convert!".format(len(failed_conversions), number_of_files))
        print("Unable to transcode the following files:")
        for file in failed_conversions:
            print("\t" + str(file))