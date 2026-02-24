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


from pathlib import Path
import re
from typing import Union


class TransmuteInfo:
    """
    This class manages the information about which files to
    transmute. It manages a (sorted) list of tuples: (pattern, script)
    to indicate which pattern will trigger the use of which PSyclone
    script. The 'pattern' is checked using a simple substring operation,
    e.g. "science/ukca"

    For now, it reads the content of psyclone_transmute_file_list.mk
    to get the required data.
    TODO: change this to a yaml file.

    """
    ALL_SECTIONS = ["PSYCLONE_PHYSICS_FILES",
                    "PSYCLONE_DIRECTORIES",
                    "PSYCLONE_PHYSICS_EXCEPTION"]

    def __init__(self):
        self._vars = {}
        # A list of ('pattern', 'script') pairs, indicating
        # which PSyclone script to use for which pattern, whicn
        # can be a filename, directories, ...
        self._pattern_to_script: list[tuple(str, str)] = []

    def import_makefile(self, filename: str, mode: str) -> None:
        """
        This method reads in a makefile which defines variables, e.g.
            export PSYCLONE_PHYSICS_FILES = mphys_kernel_mod \
                                            bm_tau_kernel_mod ...
            export PSYCLONE_DIRECTORIES = science/ukca

        This method is to support the original makefile design, and
        can be removed later. While the original design supports an
        exclude and include mode (to select which part of the
        makefile to use: files or directories/exceptions), this
        class implements a more flexible way of determining the
        script to use for which file.

        :param filename: filename to read.
        :param mode: 'include' or 'exclude' to describe which section to
            extract from the Makefile.
        """

        mode = mode.lower()
        if mode not in ["exclude", "include"]:
            raise ValueError(f"TransmuteInfo.import_makefile expects 'include'"
                             f" or 'exclude' as mode, but got '{mode}'.")
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
            if not grps:
                # Ignore comments and empty lines
                continue

            if grps[1].upper() == "PSYCLONE_PHYSICS_FILES":
                # Only read in include mode:
                if mode == "include":
                    for pattern in grps[2].split():
                        self._pattern_to_script.append((pattern,
                                                        f"{pattern}.py"))
                continue

            if grps[1].upper() == "PSYCLONE_PHYSICS_EXCEPTION":
                # Only read in exclude mode:
                if mode == "exclude":
                    # Exception: set 'no script'
                    for pattern in grps[2].split():
                        self._pattern_to_script.append((pattern, ""))
                continue

            if grps[1].upper() == "PSYCLONE_DIRECTORIES":
                # Only read in exclude mode:
                if mode == "exclude":
                    for pattern in grps[2].split():
                        # This seems to be not well defined in current LFRic :(
                        self._pattern_to_script.append((pattern, "local.py"))
                continue

            raise ValueError(f"Unexpected line '{line}' in file"
                             f"'{filename}'.")

    def get_transmute_files(self,
                            file_set: set[Path]) -> set[Union[Path, str]]:
        """
        Filters the specified list of paths for all files that have
        a transmutation script assigned. It returns a set of tuples:
        first the path, then the script to use. If a path matches
        several pattern in a file, the last one specified will be
        returned.

        :param file_set: set of files to filter and determining the
            script to use for.

        :returns: the list of physics files which should be transmuted.

        """
        result: set[tuple[Path, str]] = set()
        for filename in file_set:
            name_str = str(filename)
            final_script = ""
            for pattern, script in self._pattern_to_script:
                if pattern in name_str:
                    final_script = script
            print("XX", filename, final_script, self._pattern_to_script)
            if final_script:
                result.add((filename, final_script))
        return result
