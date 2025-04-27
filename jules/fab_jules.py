#!/usr/bin/env python3
##############################################################################
# (c) Crown copyright Met Office. All rights reserved.
# For further details please refer to the file COPYRIGHT
# which you should have received as part of this distribution
##############################################################################

'''This module contains a BAF-based build script for jules.
'''


import logging
from typing import List

from baf_base import BafBase
from fab.steps.find_source_files import find_source_files, Exclude
from fab.steps.grab.fcm import fcm_export
from fab.steps.root_inc_files import root_inc_files


class JulesBuild(BafBase):
    '''A class to build Jules using BAF as base class.

    :parameter name: name of the build.
    :parameter revision: the revision of Jules to extract.
    '''

    def __init__(self, name: str, revision: str):
        '''Build jules using Fab.

        :param name: the name for the fab workspace.
        :param revision: the revision to use
        '''
        self._revision = revision
        super().__init__(name)

    def grab_files(self):
        '''Extracts all the required source files from the repositories.
        '''
        fcm_export(self.config, src='fcm:jules.xm_tr/src',
                   revision=self._revision, dst_label='src')
        fcm_export(self.config, src='fcm:jules.xm_tr/utils',
                   revision=self._revision, dst_label='utils')

    def find_source_files(self):
        '''Finds all the sources files to analyse.
        '''
        path_filters = [
            Exclude('src/control/um/'),
            Exclude('src/initialisation/um/'),
            Exclude('src/control/rivers-standalone/'),
            Exclude('src/initialisation/rivers-standalone/'),
            Exclude('src/params/shared/cable_maths_constants_mod.F90'),
        ]

        find_source_files(self.config, path_filters=path_filters)

        # move inc files to the root for easy tool use
        root_inc_files(self.config)

    def define_preprocessor_flags(self):
        '''Defines the preprocessor flags.
        TODO: This uses a BAF private attribute, this must be
        done properly.
        '''
        super().define_preprocessor_flags()
        self.set_flags(['-P', '-DMPI_DUMMY', '-DNCDF_DUMMY', '-I$output'],
                       self._preprocessor_flags)

    def get_linker_flags(self) -> List[str]:
        '''Base class for setting linker flags.
        :returns: list of flags for the linker.
        '''
        libs = ['netcdf', 'hdf5']
        return libs


if __name__ == '__main__':
    logger = logging.getLogger('fab')
    logger.setLevel(logging.DEBUG)

    # TODO: Ideally, the version number should be added as command line
    # option by overwriting define_command_line_options and
    # handle_command_line_options
    jb = JulesBuild("jules", revision="vn6.3")
    jb.build()
