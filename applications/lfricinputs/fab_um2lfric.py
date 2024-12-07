#!/usr/bin/env python3
# ##############################################################################
#  (c) Crown copyright Met Office. All rights reserved.
#  For further details please refer to the file COPYRIGHT
#  which you should have received as part of this distribution
# ##############################################################################

'''A FAB build script for lfricinputs-um2lfric. It relies on
the LFRicBase class contained in the infrastructure directory.
'''

import logging

from fab.steps.grab.fcm import fcm_export
from fab.steps.grab.folder import grab_folder
from fab.build_config import AddFlags
from fab.steps.find_source_files import Exclude, Include

from lfric_base import LFRicBase

from fcm_extract import FcmExtract


class FabLfricInputs(LFRicBase):

    def define_preprocessor_flags(self):
        super().define_preprocessor_flags()

        self.set_flags(
            ['-DUM_PHYSICS',
             '-DCOUPLED', '-DUSE_MPI=YES'], self._preprocessor_flags)

    def grab_files(self):
        super().grab_files()
        dirs = ['applications/lfricinputs/source/um2lfric',
                'applications/lfricinputs/source/common',
                'science/um_physics_interface/source/',
                'science/jules_interface/source/',
                'science/socrates_interface/source/',
                'science/gungho/source',
                ]

        # pylint: disable=redefined-builtin
        for dir in dirs:
            grab_folder(self.config, src=self.lfric_apps_root / dir,
                        dst_label=dir)

        fcm_export(self.config, src=f'fcm:shumlib.xm_tr',
                   dst_label=f'shumlib')

    def find_source_files(self):
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

        super().find_source_files(path_filters=path_filters)

    def get_rose_meta(self):
        return (self.lfric_apps_root / 'science' / 'gungho' / 'rose-meta' /
                'lfric-gungho' / 'HEAD' / 'rose-meta.conf')

    def preprocess_c(self):
        path_flags = [AddFlags(match="$source/science/um/*",
                               flags=['-I$relative/include',
                                      '-I/$source/science/\
                                        um/include/other/',
                                      '-I$source/science/\
                                        shumlib/common/src',
                                      '-I$source/science/shumlib/\
                                        shum_thread_utils/src',]),
                      AddFlags(match="$source/science/jules/*",
                               flags=['-DUM_JULES', '-I$output']),
                      AddFlags(match="$source/shumlib/*",
                               flags=['-DSHUMLIB_LIBNAME=libshum',
                                      '-I$output',
                                      '-I$source/shumlib/common/src',
                                      '-I$source/shumlib/\
                                        shum_thread_utils/src',
                                      '-I$relative'],),
                      AddFlags(match="$source/science/8",
                               flags=['-DLFRIC'])]
        super().preprocess_c(path_flags=path_flags)

    def preprocess_fortran(self):
        path_flags = [AddFlags(match="$source/science/um/*",
                               flags=['-I$relative/include',
                                      '-I$source/shumlib/\
                                       shum_thread_utils/src/']),
                      AddFlags(match="$source/science/jules/*",
                               flags=['-DUM_JULES', '-I$output']),
                      AddFlags(match="$source/science/shumlib/*",
                               flags=['-DSHUMLIB_LIBNAME=libshum',
                                      '-I$output',
                                      '-I$source/shumlib/common/src',
                                      '-I$relative'],),
                      AddFlags(match="$source/science/*",
                               flags=['-DLFRIC'])]
        super().preprocess_fortran(path_flags=path_flags)


# -----------------------------------------------------------------------------
if __name__ == '__main__':

    logger = logging.getLogger('fab')
    logger.setLevel(logging.DEBUG)
    fab_lfric_inputs = FabLfricInputs(name="lfric_inputs",
                                      root_symbol="um2lfric")
    fab_lfric_inputs.build()
