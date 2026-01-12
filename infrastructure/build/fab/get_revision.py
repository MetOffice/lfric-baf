#!/usr/bin/env python3
##############################################################################
# (c) Crown copyright Met Office. All rights reserved.
# For further details please refer to the file COPYRIGHT
# which you should have received as part of this distribution
##############################################################################

'''
This module contains a function that extracts the revision numbers
from a dependencies.yaml file.
'''
from pathlib import Path
from typing import Union
import yaml


class GetRevision(dict):
    '''
    A simple dictionary-like class that stores the version information
    from a yaml file:

        casim:
            source: git@github.com:MetOffice/casim.git
            ref: 2025.12.1
        ...

    The information can be accessed as a dictionary, e.g.:
        gr = GetRevision("$LFRIC_APPS_SRC/dependencies.yaml")
        gr["casim"] --> {"source": "git@.../casim.git",
                         "ref": "2025.12.1"}

    The constructor will check that each dependency has indeed
    source and ref defined (not that for lfric_apps these are
    defined, but empty, indicating to use the current directory).

    If the requested section does not exist, a key error is raised.

    :param filename: The path to the dependencies.yaml file.
    '''

    def __init__(self, filename: Union[str, Path]) -> None:
        super().__init__()
        with open(filename, "r", encoding="utf8") as stream:
            dependencies = yaml.safe_load(stream)

        for repo in dependencies:
            if "source" not in dependencies[repo]:
                raise RuntimeError(f"'{filename} does not contain a 'source' "
                                   f"definition for repo '{repo}'.")
            if "ref" not in dependencies[repo]:
                raise RuntimeError(f"'{filename} does not contain a 'ref' "
                                   f"definition for repo '{repo}'.")
            self[repo] = dependencies[repo]

    def get_source(self, repo: str) -> str:
        """
        :returns: the source URL for the specified repository.

        :raises:KeyError if the repository is not defined.
        """
        return self[repo]["source"]

    def get_ref(self, repo: str) -> str:
        """
        :returns: the reference for the specified repository.

        :raises:KeyError if the repository is not defined.
        """
        return self[repo]["ref"]
