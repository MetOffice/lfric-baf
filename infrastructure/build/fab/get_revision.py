#!/usr/bin/env python3
##############################################################################
# (c) Crown copyright Met Office. All rights reserved.
# For further details please refer to the file COPYRIGHT
# which you should have received as part of this distribution
##############################################################################

'''
This module contains a function that extracts the revision numbers
from a dependencies.sh file.
'''
from pathlib import Path
import re
from typing import Union


class GetRevision(dict):
    '''
    A simple dictionary-like class that stores the version information
    from a parameter.sh file:
        export casim_rev=um13.4
        export socrates_rev=1483
    The information can be accessed as a dictionary, e.g.:
        gr = GetRevision("$LFRIC_APPS_SRC/dependencies.sh")
        gr["casim"] --> "um13.4"
        gr["socrates"] --> "1483"
    If the requested section does not exist, a key error is raised.

    :param filename: The path to the dependencies.sh file.
    '''

    def __init__(self, filename: Union[str, Path]) -> None:
        super().__init__()
        re_revision = re.compile(r"^ *export ([a-z0-0_]+)_rev *= *(.*)$")
        with open(filename, encoding="utf8") as f_in:
            for line in f_in.readlines():
                grp = re_revision.match(line)
                if grp:
                    lib = grp.group(1).lower()
                    self[lib] = grp.group(2)
