#!/usr/bin/env python3
# ##############################################################################
#  (c) Crown copyright Met Office. All rights reserved.
#  For further details please refer to the file COPYRIGHT
#  which you should have received as part of this distribution
# ##############################################################################

'''A FAB build script for lfric_atm. It relies on the LFRicBase class
contained in the infrastructure directory.
'''

import logging

from fab.steps.grab.fcm import fcm_export
from fab.steps.grab.folder import grab_folder
from fab.build_config import AddFlags
from fab.steps.find_source_files import Exclude, Include
from fab.tools import Category

from lfric_base import LFRicBase
from get_revision import GetRevision

from fcm_extract import FcmExtract


class FabLFRicAtm(LFRicBase):

    def define_preprocessor_flags(self):
        super().define_preprocessor_flags()

        self.set_flags(
            ['-DUM_PHYSICS',
             '-DCOUPLED', '-DUSE_MPI=YES'], self._preprocessor_flags)

    def grab_files(self):
        super().grab_files()
        dirs = ['applications/lfric_atm/source',
                'science/gungho/source',
                'science/physics_schemes/source',
                'science/shared/source/',
                'interfaces/coupled_interface/source/',
                'interfaces/jules_interface/source/',
                'interfaces/physics_schemes_interface/source/',
                'interfaces/socrates_interface/source/',
                # for backward compatibility
                'science/coupled_interface/source/',
                'science/um_physics_interface/source/',
                'science/socrates_interface/source/',
                'science/jules_interface/source/',
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

        gr = GetRevision("../../dependencies.sh")
        xm = "xm"
        for lib, revision in gr.items():
            # Shumlib has no src directory
            if lib == "shumlib":
                src = ""
            else:
                src = "/src"
            print(f'fcm:{lib}.{xm}_tr{src}', f'science/{lib}', revision)
            fcm_export(self.config, src=f'fcm:{lib}.{xm}_tr/{src}',
                       dst_label=f'science/{lib}', revision=revision)

        # Copy the optimisation scripts into a separate directory
        dir = 'applications/lfric_atm/optimisation'
        grab_folder(self.config, src=self.lfric_apps_root / dir,
                    dst_label='optimisation')

    def find_source_files(self):
        """Based on $LFRIC_APPS_ROOT/build/extract/extract.cfg"""

        extract_cfg = [FcmExtract(self.lfric_apps_root / "build" / "extract" /
                                  "extract.cfg")]

        socrates_extract_cfg = (self.lfric_apps_root / "interfaces" /
                               "socrates_interface" / "build" /
                               "extract.cfg")
        if socrates_extract_cfg.exists():
           extract_cfg.append(FcmExtract(socrates_extract_cfg))

        jules_extract_cfg = (self.lfric_apps_root / "interfaces" /
                            "jules_interface" / "build" /
                            "extract.cfg")
        if jules_extract_cfg.exists():
           extract_cfg.append(FcmExtract(jules_extract_cfg))

        # for backward compatibility
        socrates_extract_cfg = (self.lfric_apps_root / "science" /
                               "socrates_interface" / "build" /
                               "extract.cfg")
        if socrates_extract_cfg.exists():
           extract_cfg.append(FcmExtract(socrates_extract_cfg))

        jules_extract_cfg = (self.lfric_apps_root / "science" /
                            "jules_interface" / "build" /
                            "extract.cfg")
        if jules_extract_cfg.exists():
           extract_cfg.append(FcmExtract(jules_extract_cfg))

        science_root = self.config.source_root / 'science'
        path_filters = []
        for extract in extract_cfg:
            for section, source_file_info in extract.items():
                for (list_type, list_of_paths) in source_file_info:
                    if list_type == "exclude":
                        path_filters.append(Exclude(science_root / section))
                    else:
                        # Remove the 'src' which is the first part of the name
                        new_paths = [i.relative_to(i.parents[-2])
                                     for i in list_of_paths]
                        for path in new_paths:
                            path_filters.append(Include(science_root /
                                                        section / path))
        super().find_source_files(path_filters=path_filters)

    def get_rose_meta(self):
        return (self.lfric_apps_root / 'applications/lfric_atm' / 'rose-meta' /
                'lfric-lfric_atm' / 'HEAD' / 'rose-meta.conf')

    def preprocess_c(self):
        path_flags = [AddFlags(match="$source/science/jules/*",
                               flags=['-DUM_JULES', '-I$output']),
                      AddFlags(match="$source/science/shumlib/*",
                               flags=['-DSHUMLIB_LIBNAME=libshum',
                                      '-I$output',
                                      '-I$source/science/shumlib/common/src',
                                      '-I$source/science/shumlib/\
                                        shum_thread_utils/src',
                                      '-I$relative'],),
                      AddFlags(match="$source/science/8",
                               flags=['-DLFRIC']),
                      AddFlags(match="$source/atmosphere_service/*",
                               flags=['-I$relative/include',
                                      '-I$source/science/shumlib/common/src',
                                      '-I$source/science/shumlib/\
                                        shum_thread_utils/src',]),         
                      AddFlags(match="$source/boundary_layer/*",
                               flags=['-I$relative/include',
                                      '-I$source/science/shumlib/common/src',
                                      '-I$source/science/shumlib/\
                                        shum_thread_utils/src',]),         
                      AddFlags(match="$source/large_scale_precipitation/*",
                               flags=['-I$relative/include',
                                      '-I$source/science/shumlib/common/src',
                                      '-I$source/science/shumlib/\
                                        shum_thread_utils/src',]),         
                      AddFlags(match="$source/free_tracers/*",
                               flags=['-I$relative/include',
                                      '-I$source/science/shumlib/common/src',
                                      '-I$source/science/shumlib/\
                                        shum_thread_utils/src',]),  
                      # for backward compatibility
                      AddFlags(match="$source/science/um/*",
                               flags=['-I$relative/include',
                                      '-I/$source/science/um/include/other/',
                                      '-I$source/science/shumlib/common/src',
                                      '-I$source/science/shumlib/\
                                        shum_thread_utils/src',]),       
                     ]
        super().preprocess_c(path_flags=path_flags)

    def preprocess_fortran(self):
        path_flags = [AddFlags(match="$source/science/jules/*",
                               flags=['-DUM_JULES', '-I$output']),
                      AddFlags(match="$source/science/shumlib/*",
                               flags=['-DSHUMLIB_LIBNAME=libshum',
                                      '-I$output',
                                      '-I$source/shumlib/common/src',
                                      '-I$relative'],),
                      AddFlags(match="$source/science/*",
                               flags=['-DLFRIC']),
                      AddFlags(match="$source/atmosphere_service/*",
                               flags=['-I$relative/include',
                                      '-I$source/shumlib/\
                                        shum_thread_utils/src/']),
                      AddFlags(match="$source/boundary_layer/*",
                               flags=['-I$relative/include',
                                      '-I$source/shumlib/\
                                        shum_thread_utils/src/']),
                      AddFlags(match="$source/large_scale_precipitation/*",
                               flags=['-I$relative/include',
                                      '-I$source/shumlib/\
                                        shum_thread_utils/src/']),
                      AddFlags(match="$source/free_tracers/*",
                               flags=['-I$relative/include',
                                      '-I$source/shumlib/\
                                        shum_thread_utils/src/']),
                      # for backward compatibility
                      AddFlags(match="$source/science/um/*",
                               flags=['-I$relative/include',
                                      '-I$source/shumlib/\
                                        shum_thread_utils/src/']),
                     ]
        super().preprocess_fortran(path_flags=path_flags)

    def compile_fortran(self):
        fc = self.config.tool_box[Category.FORTRAN_COMPILER]
        # TODO: needs a better solution, we are still hardcoding compilers here
        if fc.suite == "intel-classic":
            no_omp = "-qno-openmp"
            real8 = "-r8"
            no_externals = ["-warn", "noexternals"]
            # Some SOCRATES functions do not currently declare interfaces
            # This avoids a warning-turned-error about missing interfaces
        else:
            no_omp = "-fno-openmp"
            real8 = "-fdefault-real-8"
            no_externals = []
        path_flags = [AddFlags(
            '$output/science/um/atmosphere/large_scale_precipitation/*',
            [no_omp]),
            AddFlags(match="$output/science/*", flags=[real8]),
            AddFlags(match="$output/jules/*", flags=[real8]),
            AddFlags(match="$output/socrates/*", flags=[real8]),
            AddFlags(match="$output/legacy/*", flags=[real8]),
            AddFlags(match="$output/AC_assimilation/*", flags=[real8]),
            AddFlags(match="$output/aerosols/*", flags=[real8]),
            AddFlags(match="$output/atmosphere_service/*", flags=[real8]),
            AddFlags(match="$output/boundary_layer/*", flags=[real8]),
            AddFlags(match="$output/carbon/*", flags=[real8]),
            AddFlags(match="$output/convection/*", flags=[real8]),
            AddFlags(match="$output/diffusion_and_filtering/*", flags=[real8]),
            AddFlags(match="$output/dynamics/*", flags=[real8]),
            AddFlags(match="$output/dynamics_advection/*", flags=[real8]),
            AddFlags(match="$output/electric/*", flags=[real8]),
            AddFlags(match="$output/free_tracers/*", flags=[real8]),
            AddFlags(match="$output/gravity_wave_drag/*", flags=[real8]),
            AddFlags(match="$output/idealised/*", flags=[real8]),
            AddFlags(match="$output/large_scale_cloud/*", flags=[real8]),
            AddFlags(match="$output/large_scale_precipitation/*", flags=[real8]),
            AddFlags(match="$output/PWS_diagnostics/*", flags=[real8]),
            AddFlags(match="$output/radiation_control/*", flags=[real8]),
            AddFlags(match="$output/stochastic_physics/*", flags=[real8]),
            AddFlags(match="$output/tracer_advection/*", flags=[real8]),
            AddFlags(match="$output/science/socrates/radiance_core/*",
                     flags=no_externals),
            AddFlags(match="$output/science/socrates/interface_core/*",
                     flags=no_externals)]
        # TODO: A remove flag functionality based on profile option
        # and precision is needed
        if self._args.profile == 'full-debug':
            self._compiler_flags.remove('-check all,noshape') \
                if '-check all,noshape' in self._compiler_flags \
                else self._compiler_flags.remove('-check all')
        super().compile_fortran(path_flags=path_flags)


# -----------------------------------------------------------------------------
if __name__ == '__main__':

    logger = logging.getLogger('fab')
    logger.setLevel(logging.DEBUG)
    fab_lfric_atm = FabLFRicAtm(name="lfric_atm")
    fab_lfric_atm.build()
