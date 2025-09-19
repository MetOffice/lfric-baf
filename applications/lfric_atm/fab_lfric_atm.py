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
from typing import List

from fab.steps.grab.fcm import fcm_export
from fab.steps.grab.folder import grab_folder
from fab.build_config import AddFlags
from fab.steps.find_source_files import Exclude, Include
from fab.tools import Category

from lfric_base import LFRicBase
from get_revision import GetRevision

from fcm_extract import FcmExtract


class FabLFRicAtm(LFRicBase):

    def define_preprocessor_flags_step(self):
        super().define_preprocessor_flags_step()

        self.add_preprocessor_flags(
            ['-DUM_PHYSICS',
             '-DLFRIC',
             '-DUSSPPREC_32B',
             '-DLSPREC_32B',])

        path_flags = [AddFlags(match="$source/science/jules/*",
                               flags=['-DUM_JULES', '-I$output']),
                      AddFlags(match="$source/science/shumlib/*",
                               flags=['-DSHUMLIB_LIBNAME=libshum',
                                      '-I$output',
                                      '-I$source/science/shumlib/common/src',
                                      '-I$source/science/shumlib/\
                                        shum_thread_utils/src',
                                      '-I$relative'],),
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
        self.add_preprocessor_flags(path_flags)

    def get_linker_flags(self) -> List[str]:
        '''
        This method adds shumlib to the lfric_base class get_linker_flags return. 

        :returns: list of flags for the linker.
        :rtype: List[str]
        '''
        libs = ['shumlib', ]
        return libs + super().get_linker_flags()

    def grab_files_step(self):
        super().grab_files_step()
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

    def find_source_files_step(self):
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
        super().find_source_files_step(path_filters=path_filters)

    def get_rose_meta(self):
        return (self.lfric_apps_root / 'applications/lfric_atm' / 'rose-meta' /
                'lfric-lfric_atm' / 'HEAD' / 'rose-meta.conf')

    def analyse_step(self):
        '''
        The method adds lfric_atm specific list of dependencies to ignore.
        This list of shumlib may be used by developers during debugging.
        '''
        lfric_atm_ignore_dependencies = ['c_shum_byteswap.o', 'f_shum_is_nan_mod',
                                        'f_shum_field_mod', 'f_shum_is_inf_mod',
                                        'f_shum_file_mod', 'f_shum_is_denormal_mod']
        super().analyse_step(ignore_dependencies=lfric_atm_ignore_dependencies)

    def compile_fortran_step(self):
        fc = self.config.tool_box[Category.FORTRAN_COMPILER]
        profile = self.config.profile
        no_omp = []
        no_externals = []
        path_flags = []
        # TODO: needs a better solution, we are still hardcoding compilers here
        if fc.suite == "intel-classic":
            no_omp = ["-qno-openmp"]
            um_physics = ["-r8"]
            no_externals = ["-warn", "noexternals"]
            # Some SOCRATES functions do not currently declare interfaces
            # This avoids a warning-turned-error about missing interfaces
        elif fc.suite == "cray":
            um_physics = ["-s", "real64"]
            ovewrite_debug_optimisation = []
            if profile == "fast-debug":
                ovewrite_debug_optimisation = ["-O0", "-G0"]
                path_flags += [AddFlags(match='$output/*parcel_ascent_5a*',
                                        flags=["-s", "real64", "-hvector0"]),
                               AddFlags(match='$output/large_scale_precipitation/*',
                                        flags=["-O2", "-hfp0", "-hflex_mp=strict"])]
            if profile == "production":
                ovewrite_debug_optimisation = ["-O0"]
                path_flags += [AddFlags(match='$output/gravity_wave_drag/*',
                                        flags=["-O2", "-hflex_mp=strict"]),
                               AddFlags(match='$output/*parcel_ascent_5a*',
                                        flags=["-s", "real64", "-hvector0"]),
                               AddFlags(match='$output/large_scale_precipitation/*',
                                        flags=["-O3", "-hipa3", "-hflex_mp=conservative"])]
            path_flags += [AddFlags(match='$output/*ukca_emiss_mode_mod*',
                                    flags=ovewrite_debug_optimisation),
                           AddFlags(match='$output/*ukca_step_control_mod*',
                                    flags=ovewrite_debug_optimisation),
                           AddFlags(match='$output/*aerosol_ukca_alg_mod_psy*',
                                    flags=ovewrite_debug_optimisation),
                           AddFlags(match='$output/*bl_exp_alg_mod_psy*',
                                    flags=ovewrite_debug_optimisation),
                           AddFlags(match='$output/*bl_imp_alg_mod_psy*',
                                    flags=ovewrite_debug_optimisation),
                           AddFlags(match='$output/*conv_comorph_alg_mod_psy*',
                                    flags=ovewrite_debug_optimisation),
                           AddFlags(match='$output/*conv_comorph_kernel_mod*',
                                    flags=ovewrite_debug_optimisation),
                           AddFlags(match='$output/*conv_gr_alg_mod_psy*',
                                    flags=ovewrite_debug_optimisation),
                           AddFlags(match='$output/*gungho_model_mod*',
                                    flags=ovewrite_debug_optimisation),
                           AddFlags(match='$output/*init_aerosol_fields_alg_mod_psy*',
                                    flags=ovewrite_debug_optimisation),
                           AddFlags(match='$output/*jules_extra_kernel_mod*',
                                    flags=ovewrite_debug_optimisation),]
        else:
            no_omp = ["-fno-openmp"]
            um_physics = ["-fdefault-real-8"]
        path_flags += [
            AddFlags(match='$output/science/um/atmosphere/large_scale_precipitation/*',
            flags=no_omp),
            AddFlags(match="$output/science/*", flags=um_physics),
            # jules and socrates are extracted in the science folder
            AddFlags(match="$output/legacy/*", flags=um_physics),
            AddFlags(match="$output/AC_assimilation/*", flags=um_physics),
            AddFlags(match="$output/aerosols/*", flags=um_physics),
            AddFlags(match="$output/atmosphere_service/*", flags=um_physics),
            AddFlags(match="$output/boundary_layer/*", flags=um_physics),
            AddFlags(match="$output/carbon/*", flags=um_physics),
            AddFlags(match="$output/convection/*", flags=um_physics),
            AddFlags(match="$output/diffusion_and_filtering/*", flags=um_physics),
            AddFlags(match="$output/dynamics/*", flags=um_physics),
            AddFlags(match="$output/dynamics_advection/*", flags=um_physics),
            AddFlags(match="$output/electric/*", flags=um_physics),
            AddFlags(match="$output/free_tracers/*", flags=um_physics),
            AddFlags(match="$output/gravity_wave_drag/*", flags=um_physics),
            AddFlags(match="$output/idealised/*", flags=um_physics),
            AddFlags(match="$output/large_scale_cloud/*", flags=um_physics),
            AddFlags(match="$output/large_scale_precipitation/*",
                     flags=um_physics),
            AddFlags(match="$output/PWS_diagnostics/*", flags=um_physics),
            AddFlags(match="$output/radiation_control/*", flags=um_physics),
            AddFlags(match="$output/stochastic_physics/*", flags=um_physics),
            AddFlags(match="$output/tracer_advection/*", flags=um_physics),
            AddFlags(match="$output/science/socrates/radiance_core/*",
                     flags=no_externals),
            AddFlags(match="$output/science/socrates/interface_core/*",
                     flags=no_externals)]
        super().compile_fortran_step(path_flags=path_flags)


# -----------------------------------------------------------------------------
if __name__ == '__main__':

    logger = logging.getLogger('fab')
    logger.setLevel(logging.DEBUG)
    fab_lfric_atm = FabLFRicAtm(name="lfric_atm")
    fab_lfric_atm.build()
