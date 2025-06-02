#!/usr/bin/env python3
##############################################################################
# (c) Crown copyright Met Office. All rights reserved.
# For further details please refer to the file COPYRIGHT
# which you should have received as part of this distribution
##############################################################################

'''
This module contains a BAF-based build script for Gcom.
'''

import argparse
import logging
from typing import cast, Optional

from baf_base import BafBase

from fab.steps.find_source_files import Exclude, find_source_files
from fab.steps.grab.fcm import fcm_export
from fab.steps.grab.git import git_checkout


class GcomBuild(BafBase):
    '''
    A class to build Gcom using BAF as base class.

    :param str name: name of the build.
    '''

    def __init__(self, name: str):
        '''
        Build Gcom using Fab. It stores the revision number,
        so it can be used in the grab_files step.
        '''
        # This attribute points to the actual gcom source directory
        # since this directory is different between a git and svn
        # version.
        self._source_root = None
        self._branch = None
        super().__init__(name, link_target="static-library")

    def define_command_line_options(
            self,
            parser: Optional[argparse.ArgumentParser] = None
            ) -> argparse.ArgumentParser:
        '''
        This adds a revision option to the command line options inherited
        from the base class.

        :param parser: a pre-defined argument parser. If not, a new instance
            will be created.
        :returns: the argument parser with the Gcom specific options added.
        '''

        parser = super().define_command_line_options(parser)
        parser = cast(argparse.ArgumentParser, parser)
        parser.add_argument(
            "--branch", "-b", type=str, default="trunk",
            help="Sets the Gcom revision to checkout.")
        return parser

    def handle_command_line_options(self,
                                    parser: argparse.ArgumentParser) -> None:
        '''
        Grab the requested (or default) Gcom revision to use and
        store it in an attribute.

        :param argparse.ArgumentParser parser: the argument parser.
        '''

        super().handle_command_line_options(parser)
        self._branch = self.args.branch

    def grab_files_step(self) -> None:
        '''
        Extracts all the required Gcom source files from the repositories.
        '''
        # Try to grab sources from GitHub, fallback to FCM if that fails
        try:
            git_checkout(
                self.config,
                src="git@github.com:MetOffice/gcom",
                revision=self._branch,
                dst_label="gcom",
            )
            self._source_root = self.config.source_root / "gcom/build"
        except Exception as e:
            logging.warning(f"git_checkout failed: {e}, "
                            f"falling back to fcm_export")
            fcm_export(
                self.config,
                src="fcm:gcom.xm_tr/build",
                revision=self._branch,
                dst_label="gcom",
            )
            self._source_root = self.config.source_root / "gcom"

    def find_source_files_step(self):
        '''
        Finds all the Gcom sources files to analyse.
        '''
        path_filters = [
            Exclude(f"{self._source_root}/sums/"),
            Exclude(f"src/gcom/test/"),
            Exclude(f"src/gcom/tune/"),
        ]

        find_source_files(self.config,
                          source_root=self._source_root,
                          path_filters=path_filters)

    def define_preprocessor_flags(self) -> None:
        '''
        Defines the preprocessor flags.
        '''
        super().define_preprocessor_flags()
        self.add_preprocessor_flags([f"-I{self._source_root}/include",
                                     '-DGC_VERSION="7.6"',
                                     '-DGC_BUILD_DATE="20220111"',
                                     '-DGC_DESCRIP="dummy desrip"',
                                     ])


# ===========================================================================
if __name__ == "__main__":
    logger = logging.getLogger("fab")
    logger.setLevel(logging.DEBUG)

    gcom = GcomBuild("gcom")
    gcom.build()
