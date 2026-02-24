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
from collections import namedtuple
from pathlib import Path
from typing import Union
import yaml


# A namedtuple to keep track of repository source and references
RepoInfo = namedtuple("RepoInfo", ["source", "ref"])


class GetRevision:
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
        self._repo_info: dict[str, list[RepoInfo]] = {}

        with open(filename, "r", encoding="utf8") as stream:
            dependencies = yaml.safe_load(stream)

        for repo, all_deps in dependencies.items():
            # A repo can either have a single definition, or a list
            # Support both:
            if not isinstance(all_deps, list):
                all_deps = [all_deps]

            self._repo_info[repo] = []
            for dep in all_deps:
                if "source" not in dep:
                    raise RuntimeError(f"'{filename} does not contain a "
                                       f"'source' definition for repo "
                                       f"'{repo}'.")
                if "ref" not in dep:
                    raise RuntimeError(f"'{filename} does not contain a "
                                       f"'ref' definition for repo '{repo}'.")
                self._repo_info[repo].append(RepoInfo(dep["source"],
                                                      dep["ref"]))

    def get_repo_names(self) -> list[str]:
        """
        :returns: the list of all repositories stored in this object.
        """
        return list(self._repo_info.keys())

    def get_repo_info(self, repo: str) -> list[RepoInfo]:
        """
        :returns: the list of repository infos for a given dependency.

        :raises:KeyError if the repository is not defined.
        """
        return self._repo_info[repo]
