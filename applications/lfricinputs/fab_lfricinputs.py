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
from typing import List, Union

from fab.steps.grab.fcm import fcm_export
from fab.steps.grab.folder import grab_folder
from fab.build_config import AddFlags
from fab.steps.find_source_files import Exclude, Include

from lfric_base import LFRicBase

from fcm_extract import FcmExtract


class FabLfricInputs(LFRicBase):
    '''
    This class builds LFRic inputs. Since LFRic inputs builds
    different binaries in the same tree, it explicitly adds
    the list of target symbols to build.

    :param name: The name of the project directory.
    :param root_symbol: The symbol of the main program(s) to be
        created.
    '''

    def __init__(self, name: str, root_symbol: Union[str, List[str]]):
        super().__init__(name)
        self.set_root_symbol(root_symbol)

    def define_preprocessor_flags_step(self):
        super().define_preprocessor_flags_step()

        self.add_preprocessor_flags(
            ['-DUM_PHYSICS',
             '-DCOUPLED', '-DUSE_MPI=YES'])
        path_flags = [AddFlags(match="$source/science/jules/*",
                               flags=['-DUM_JULES', '-I$output']),
                      AddFlags(match="$source/shumlib/*",
                               flags=['-DSHUMLIB_LIBNAME=libshum',
                                      '-I$output',
                                      '-I$source/shumlib/common/src',
                                      '-I$source/shumlib/'
                                      'shum_thread_utils/src',
                                      '-I$relative'],),
                      AddFlags(match="$source/*",
                               flags=['-DLFRIC']),
                      AddFlags(match="$source/atmosphere_service/*",
                               flags=['-I$relative/include',
                                      '-I$source/science/shumlib/common/src',
                                      '-I$source/science/shumlib/'
                                      'shum_thread_utils/src',]),
                      AddFlags(match="$source/boundary_layer/*",
                               flags=['-I$relative/include',
                                      '-I$source/science/shumlib/common/src',
                                      '-I$source/science/shumlib/'
                                      'shum_thread_utils/src',]),
                      AddFlags(match="$source/large_scale_precipitation/*",
                               flags=['-I$relative/include',
                                      '-I$source/science/shumlib/common/src',
                                      '-I$source/science/shumlib/'
                                      'shum_thread_utils/src',]),
                      AddFlags(match="$source/free_tracers/*",
                               flags=['-I$relative/include',
                                      '-I$source/science/shumlib/common/src',
                                      '-I$source/science/shumlib/'
                                      'shum_thread_utils/src',]),
                      # for backward compatibility
                      AddFlags(match="$source/science/um/*",
                               flags=['-I$relative/include',
                                      '-I/$source/science/'
                                      'um/include/other/',
                                      '-I$source/science/'
                                      'shumlib/common/src',
                                      '-I$source/science/shumlib/'
                                      'shum_thread_utils/src',]),
                      ]

        self.add_preprocessor_flags(path_flags)

    def grab_files_step(self):
        super().grab_files_step()
        dirs = ['applications/lfricinputs/source/',
                'interfaces/jules_interface/source/',
                'interfaces/physics_schemes_interface/source/',
                'interfaces/socrates_interface/source/',
                'science/physics_schemes/source',
                'science/gungho/source',
                # for backward compatibility
                'science/um_physics_interface/source/',
                'science/jules_interface/source/',
                'science/socrates_interface/source/',
                ]

        # pylint: disable=redefined-builtin
        for dir in dirs:
            try:
                grab_folder(self.config,
                            src=self.lfric_apps_root / dir,
                            dst_label='')
            except:
                # for backward compatibility
                continue

        fcm_export(self.config, src="fcm:shumlib.xm_tr",
                   dst_label="shumlib")

    def find_source_files_step(self):
        """Based on $LFRIC_APPS_ROOT/applications/lfricinputs/fcm-make"""

        shumlib_extract = FcmExtract(self.lfric_apps_root / "applications" /
                                     "lfricinputs" / "fcm-make" / "util" /
                                     "common" / "extract-shumlib.cfg")
        shumlib_root = self.config.source_root / 'science'
        path_filters = []
        for section, source_file_info in shumlib_extract.items():
            for (list_type, list_of_paths) in source_file_info:
                if list_type == "exclude":
                    path_filters.append(Exclude(shumlib_root / section))
                else:
                    for path in list_of_paths:
                        path_filters.append(Include(shumlib_root /
                                                    section / path))

        infra_extract = FcmExtract(self.lfric_apps_root / "applications" /
                                   "lfricinputs" / "fcm-make" / "util" /
                                   "common" / "extract-lfric-core.cfg")

        infra_extract.update(FcmExtract(self.lfric_apps_root /
                                        "applications" / "lfricinputs" /
                                        "fcm-make" / "util" /
                                        "common" / "extract-lfric-apps.cfg"))

        for section, source_file_info in infra_extract.items():
            for (list_type, list_of_paths) in source_file_info:
                if list_type == "exclude":
                    path_filters.append(
                        Exclude(self.config.source_root / section))
                else:
                    for path in list_of_paths:
                        print("TTT", self.config.source_root/path)
                        path_filters.append(
                            Include(self.config.source_root / path))

        super().find_source_files_step(path_filters=path_filters)

    def get_rose_meta(self):
        return (self.lfric_apps_root / 'science' / 'gungho' / 'rose-meta' /
                'lfric-gungho' / 'HEAD' / 'rose-meta.conf')


# -----------------------------------------------------------------------------
if __name__ == '__main__':

    logger = logging.getLogger('fab')
    logger.setLevel(logging.DEBUG)
    fab_lfric_inputs = FabLfricInputs(name="lfric_inputs", root_symbol=[
        'um2lfric', 'lfric2um', 'scintelapi'])
    fab_lfric_inputs.build()
    executable_folder_path = fab_lfric_inputs.config.project_workspace
    os.rename(os.path.join(executable_folder_path, "um2lfric"),
              os.path.join(executable_folder_path, "um2lfric.exe"))
    os.rename(os.path.join(executable_folder_path, "lfric2um"),
              os.path.join(executable_folder_path, "lfric2um.exe"))
    os.rename(os.path.join(executable_folder_path, "scintelapi"),
              os.path.join(executable_folder_path, "scintelapi.exe"))
