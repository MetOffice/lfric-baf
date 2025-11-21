#!/usr/bin/env python3
# ##############################################################################
#  (c) Crown copyright Met Office. All rights reserved.
#  For further details please refer to the file COPYRIGHT
#  which you should have received as part of this distribution
# ##############################################################################

'''A FAB build script for lfricinputs. It relies on the LFRicBase class
contained in the infrastructure directory.
'''

import logging
import os
from pathlib import Path
from typing import Iterable, List, Optional, Union

from fab.steps.grab.folder import grab_folder
from fab.build_config import AddFlags

from lfric_base import LFRicBase


class FabLFRicInputs(LFRicBase):
    '''
    This class builds LFRic inputs. Since LFRic inputs builds
    different binaries in the same tree, it explicitly adds
    the list of target symbols to build.

    :param name: The name of the project directory.
    :param root_symbol: The symbol of the main program(s) to be
        created.
    '''

    def __init__(self, name: str, root_symbol: Union[str, List[str]]):
        this_file = Path(__file__).resolve()
        # Store the root of this apps for later
        self._this_root = this_file.parent
        super().__init__(name, apps_root=this_file.parents[2])
        self.set_root_symbol(root_symbol)

    def define_preprocessor_flags_step(self):
        """
        Defines the preprocessor flags.
        """
        super().define_preprocessor_flags_step()

        # for backward compatibility of building shumlib from source
        path_flags = [AddFlags(match="$source/shumlib/*",
                               flags=['-DSHUMLIB_LIBNAME=libshum',
                                      '-I$output',
                                      '-I$source/shumlib/common/src',
                                      '-I$source/shumlib/'
                                      'shum_thread_utils/src',
                                      '-I$relative'],),
                      ]

        self.add_preprocessor_flags(path_flags)

    def get_linker_flags(self) -> List[str]:
        '''
        This method adds shumlib to the lfric_base class get_linker_flags
        return.

        :returns: list of flags for the linker.
        '''
        libs = ['shumlib', ]
        return libs + super().get_linker_flags()

    def grab_files_step(self):
        """
        This method overwrites the base class grab_files_step. It includes
        all source files required for LFRicInputs
        """
        super().grab_files_step()
        dirs = ['applications/lfricinputs/source/',
                'science/gungho/source',
                'science/shared/source/',
                ]

        # pylint: disable=redefined-builtin
        for dir in dirs:
            grab_folder(self.config,
                        src=self.lfric_apps_root / dir,
                        dst_label='')

        # Copy the optimisation scripts into a separate directory if it exists
        optimisation_dir = self._this_root / "optimisation"
        if optimisation_dir.exists():
            grab_folder(self.config, src=optimisation_dir,
                        dst_label='optimisation')

    def get_rose_meta(self) -> Path:
        """
        :returns: The path to the rose meta data config file.
        """
        return (self.lfric_apps_root / 'science' / 'gungho' / 'rose-meta' /
                'lfric-gungho' / 'HEAD' / 'rose-meta.conf')

    def analyse_step(self,
                     ignore_dependencies: Optional[Iterable[str]] = None,
                     find_programs: bool = False
                     ) -> None:
        '''
        The method adds lfric_inputs specific list of dependencies to ignore.

        :param ignore_dependencies: Third party Fortran module names in
            USE statements, 'DEPENDS ON' files and modules to be ignored.
        :param find_programs: if the analyse step should try to automatically
            find all program units to build.

        '''
        inputs_ignore_dependencies = [
            'c_shum_byteswap.o', 'f_shum_ff_status_mod', 'f_shum_field_mod',
            'f_shum_fieldsfile_mod', 'f_shum_file_mod',
            'f_shum_fixed_length_header_indices_mod',
            'f_shum_lookup_indices_mod', 'f_shum_stashmaster_mod'
            ]
        if ignore_dependencies:
            inputs_ignore_dependencies.extend(ignore_dependencies)
        super().analyse_step(ignore_dependencies=inputs_ignore_dependencies,
                             find_programs=find_programs)


# -----------------------------------------------------------------------------
if __name__ == '__main__':

    logger = logging.getLogger('fab')
    logger.setLevel(logging.DEBUG)
    fab_lfric_inputs = FabLFRicInputs(name="lfric_inputs", root_symbol=[
        'um2lfric', 'lfric2um', 'scintelapi'])
    fab_lfric_inputs.build()
    executable_folder_path = fab_lfric_inputs.config.project_workspace
    os.rename(os.path.join(executable_folder_path, "um2lfric"),
              os.path.join(executable_folder_path, "um2lfric.exe"))
    os.rename(os.path.join(executable_folder_path, "lfric2um"),
              os.path.join(executable_folder_path, "lfric2um.exe"))
    os.rename(os.path.join(executable_folder_path, "scintelapi"),
              os.path.join(executable_folder_path, "scintelapi.exe"))
