#!/usr/bin/env python3

'''
This module contains a class that reads in fcm extract specifications.
'''

import logging
from pathlib import Path
import re
import sys
from typing import Union

from fab.steps.find_source_files import Include, Exclude

logger = logging.getLogger(__name__)


class FcmConfiguration(dict):
    '''
    A simple class that reads in an fcm extract.cfg file and stores
    the information about excluded and included file to be used in FAB.
    It can then produce a list of Include/Exclude directive to be used
    by Fab when finding source files.

    There is one difference between the Fcm default behaviour and
    Fab's, tracked in https://github.com/MetOffice/fab/issues/471
    FCM seems to pick the 'most specific' match, while Fab picks
    the last match. E.g.:

        extract.path-excl[shumlib] = common/src/shumlib_version.c
        extract.path-incl[shumlib] = common/src

    FCM would exclude the .c file, while Fab would include it.
    Since #471 might not get fixed (since FCM is outdated), it is
    recommended to just change the order in the extract.cfg files, so
    that the most-specific matches are at the end.

    Note that Fab Include/Exclude classes only use a sub-string tests.
    For example, a line like:

        extract.path-excl[casim] = / # everything

    Would actually ignore any file containing 'casim'. Therefore, it is
    required to add a `root_path`, which is the path where the suite is
    checked out in. This `root_path` will be added when specifying the
    matching pattern, e.g. if `root_path="science/casim/src"` the above
    line becomes `science/casim/src`  (and if specific files will be ignored,
    these also use the root_path) to avoid mismatches.

    :param filename: the name of the fcm extract file to read.
    :param root_path: the path under which the suite is checked out.
    '''

    # Some static regular expressions:
    re_comment = re.compile(r"( *#.*$)")
    re_include = re.compile(r"^ *include", re.I)
    re_location = re.compile(r"^ *extract.location(\{.*\})?\[.*\] *=")
    re_files = re.compile(r"^ *(.*)_extract_files.* *= *(.*) *$")
    re_excl = re.compile(r"^ *extract\.path-excl\[(.*)\] *= *(.*) *$")
    re_incl = re.compile(r"^ *extract\.path-incl\[(.*)\] *= *(.*) *$")

    def __init__(self,
                 filename: Path,
                 root_path: Path) -> None:
        # pylint: disable=too-many-branches, too-many-statements
        # pylint: disable=too-many-locals
        super().__init__()
        self._root_path = root_path
        # Read the files, remove comments and empty lines, and handle '\'
        with filename.open(mode="r", encoding="utf8") as f_in:
            current_line = []
            for line in f_in:
                line = line.strip()
                if not line:
                    continue
                # Check for continuation lines, i.e. backslash
                # at the beginning of a line
                if line[0] == "\\":
                    line = line[1:].strip()
                comm = FcmConfiguration.re_comment.search(line)
                if comm:
                    # Remove comments
                    line = line[:comm.start()].strip()
                # Handle multi-line
                if line.endswith("\\"):
                    current_line.append(line[:-1].strip())
                    continue

                current_line.append(line)
                line = " ".join(current_line)
                current_line = []
                if not line:
                    continue
                if FcmConfiguration.re_include.match(line):
                    # Including other files are not supported
                    logger.warning(f"Ignoring include '{line}'.")
                    continue
                if FcmConfiguration.re_location.match(line):
                    # Ignore location info
                    continue
                grp = FcmConfiguration.re_files.match(line)
                if grp:
                    section = grp.group(1).lower()
                    list_of_paths = grp.group(2).split(" ")
                    if section in self:
                        self[section].append(("include", list_of_paths))
                    else:
                        self[section] = [("include", list_of_paths)]
                    continue
                grp = FcmConfiguration.re_excl.match(line)
                if grp:
                    line_type = "exclude"
                else:
                    grp = FcmConfiguration.re_incl.match(line)
                    if not grp:
                        logger.warning(f"Unexpected line: '{line}' - ignored.")
                        continue
                    line_type = "include"
                section = grp.group(1).lower()
                list_of_paths = grp.group(2).split(" ")
                if section in self:
                    self[section].append((line_type, list_of_paths))
                else:
                    self[section] = [(line_type, list_of_paths)]

    def get_include_exclude_list(
            self,
            section: str) -> list[Union[Exclude, Include]]:
        '''
        Converts the information from the read fcm file into a list of
        Include/Exclude directives.

        :returns: a list with the corresponding include/exclude instances.
        '''

        path_filters: list[Union[Exclude, Include]] = []
        source_file_info = self[section]
        section_path = Path(section)
        InOrExClass: Union[Exclude, Include]
        for (list_type, list_of_paths) in source_file_info:
            if list_type == "exclude":
                InOrExClass = Exclude
            else:
                InOrExClass = Include
            for path in list_of_paths:
                if path == "/":
                    # Appending Path("something") and  "/" using Path results
                    # in just "/", so instead add an empty string
                    path = ""
                path_filters.append(InOrExClass(self._root_path / section_path
                                                / path))

        return path_filters


# ============================================================================
def main():
    '''
    Simple wrapper to avoid pylint errors.
    '''
    fe = FcmConfiguration(Path(sys.argv[1]), root_path=Path())
    print("Sections", fe.keys())
    for section, list_of_paths in fe.items():
        print("SECTION:", section, list_of_paths)


# ============================================================================
if __name__ == "__main__":
    # Avoid pylint errors about redefinition from outer scope
    main()
