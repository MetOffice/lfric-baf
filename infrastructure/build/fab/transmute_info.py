##############################################################################
# (c) Crown copyright Met Office. All rights reserved.
# For further details please refer to the file COPYRIGHT
# which you should have received as part of this distribution
##############################################################################


"""
This module contains a class to manage transmute info.
For now, this is based on reading in the psyclone_transmute_file_list.mk.
This is expected to be replaced with a yaml file.
"""


import re


class TransmuteInfo:
    """
    This class manages the information about which files to
    transmute.
    For now, it reads the content of psyclone_transmute_file_list.mk
    to get the required data.
    TODO: change this to a yaml file.

    """
    ALL_SECTIONS = ["PSYCLONE_PHYSICS_FILES",
                    "PSYCLONE_DIRECTORIES",
                    "PSYCLONE_PHYSICS_EXCEPTION"]

    # The indices of the section in ALL_SECTIONS:
    PHYSICS_FILES = 0
    DIRECTORIES = 1
    EXCEPTIONS = 2

    def __init__(self):
        self._vars = {}

    def import_makefile(self, filename: str) -> None:
        """
        This method reads in a makefile which defines variables, e.g.
            export PSYCLONE_PHYSICS_FILES = mphys_kernel_mod \
                                            bm_tau_kernel_mod ...
            export PSYCLONE_DIRECTORIES = science/ukca

        This method is to support the original makefile design, and
        can be removed later.

        :param: filename to read
        """

        all_lines = []

        # First, read the makefile, and handle continuation markers
        with open(filename, "r", encoding="utf-8") as f:
            current_line = ""
            for line in f.readlines():
                # Remove newline
                line = line[:-1]
                if line.endswith("\\"):
                    # Append the line without "\" at the end
                    if current_line:
                        current_line = current_line + " " + line[:-1]
                    else:
                        current_line = line[:-1]
                else:
                    if current_line:
                        current_line = current_line + " " + line
                    else:
                        current_line = line
                    all_lines.append(current_line)
                    current_line = ""

        re_export = re.compile("^ *export *([a-zA-Z0-9_]+) *= *(.*$)")
        for line in all_lines:
            grps = re_export.match(line)
            if grps:
                self._vars[grps[1]] = grps[2].split()

        for section in TransmuteInfo.ALL_SECTIONS:
            if section not in self._vars:
                raise RuntimeError(f"Section '{section}' not found "
                                   f"in '{filename}'.")

    def get_transmute_files(self) -> list[str]:
        """
        :returns: the list of physics files which should be transmuted.
        """
        return self._vars[
            TransmuteInfo.ALL_SECTIONS[TransmuteInfo.PHYSICS_FILES]]

    def get_transmute_directories(self) -> list[str]:
        """
        :returns: the list of directories in which all files must be
            transmuted.
        """
        return self._vars[
            TransmuteInfo.ALL_SECTIONS[TransmuteInfo.DIRECTORIES]]

    def get_transmute_exceptions(self) -> list[str]:
        """
        :returns: the list of file exceptions from the directories.
        """
        return self._vars[
            TransmuteInfo.ALL_SECTIONS[TransmuteInfo.EXCEPTIONS]]
