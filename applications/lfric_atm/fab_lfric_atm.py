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
from pathlib import Path
import sys
from typing import cast, Iterable, List, Optional, Union

# We need to import the Apps base class:
sys.path.insert(0, str(Path(__file__).parents[2] / "build"))

from lfric_apps_base import LFRicAppsBase

from fab.build_config import AddFlags
from fab.steps.find_source_files import Exclude, Include
from fab.steps.grab.git import git_checkout
from fab.steps.grab.folder import grab_folder
from fab.tools import Category, Compiler

from get_revision import GetRevision

from extract_list import ExtractList

logger = logging.getLogger(__name__)


# TODO FAB #313
def get_lfric_atm_compile_fortran_specific_flags(
        fortran_compiler: Compiler,
        profile: str) -> List[AddFlags]:
    '''
    This function sets the lfric_atm compile_fortran specific flags based on
    compiler suite. Since compiler suite is a site decision, these flags
    actually would better not be set here. The Fab ticket #313 is going to
    address this.

    :param fortran_compiler: The Fortran compiler being used for lfric_atm.
    :param profile: The profile chosen for lfric_atm.

    :returns: List of path specific flags to be passed to compile_fortran step.
    '''
    no_omp: List[str] = []
    no_externals: List[str] = []
    path_flags: List[AddFlags] = []

    if fortran_compiler.suite == "intel-classic":
        no_omp = ["-qno-openmp"]
        um_physics = ["-r8"]
        no_externals = ["-warn", "noexternals"]
        # Some SOCRATES functions do not currently declare interfaces
        # This avoids a warning-turned-error about missing interfaces
    elif fortran_compiler.suite == "cray":
        um_physics = ["-s", "real64"]
        ovewrite_debug_optimisation = []
        if profile == "fast-debug":
            ovewrite_debug_optimisation = ["-O0", "-G0"]
            path_flags += [
                AddFlags(match='$output/*parcel_ascent_5a*',
                         flags=["-s", "real64", "-hvector0"]),
                AddFlags(match='$output/large_scale_precipitation/*',
                         flags=["-O2", "-hfp0", "-hflex_mp=strict"])
                ]
        if profile == "production":
            ovewrite_debug_optimisation = ["-O0"]
            path_flags += [
                AddFlags(match='$output/gravity_wave_drag/*',
                         flags=["-O2", "-hflex_mp=strict"]),
                AddFlags(match='$output/*parcel_ascent_5a*',
                         flags=["-s", "real64", "-hvector0"]),
                AddFlags(match='$output/large_scale_precipitation/*',
                         flags=["-O3", "-hipa3", "-hflex_mp=conservative"])
                ]
        path_flags += [
            AddFlags(match='$output/*ukca_emiss_mode_mod*',
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
                     flags=ovewrite_debug_optimisation),
            ]
    else:
        no_omp = ["-fno-openmp"]
        # Most lfric_atm dependencies contain code with implicit lossy
        # conversions and unused variables.

        um_physics = ["-fdefault-real-8", "-Wno-error=conversion"]
    path_flags += [
        AddFlags(match='$output/science/um/atmosphere/'
                       'large_scale_precipitation/*',
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
        AddFlags(match="$output/physics_diagnostics/*", flags=um_physics),
        AddFlags(match="$output/radiation_control/*", flags=um_physics),
        AddFlags(match="$output/stochastic_physics/*", flags=um_physics),
        AddFlags(match="$output/tracer_advection/*", flags=um_physics),
        AddFlags(match="$output/science/socrates/radiance_core/*",
                 flags=no_externals),
        AddFlags(match="$output/science/socrates/interface_core/*",
                 flags=no_externals)]

    return path_flags


class FabLFRicAtm(LFRicAppsBase):
    """
    This class implements a build system for LFRic atm. It relies on
    LFRicAppsBase for LFRic-specific functionality (e.g. common source
    files, running PSyclone etc).

    :param name: The name of the application.
    :param root_symbol: the symbol (or list of symbols) of the main
        programs. Defaults to the parameter `name` if not specified.
    """

    def __init__(self,
                 name: str,
                 root_symbol: Optional[Union[list[str], str]] = None) -> None:

        this_file = Path(__file__).resolve()
        self._lfric_apps_root = this_file.parents[2]
        super().__init__(name=name,
                         apps_root=self._lfric_apps_root,
                         root_symbol=root_symbol)
        # Store the root of this apps for later
        self._this_root = this_file.parent

    def define_preprocessor_flags_step(self):
        """
        This method overwrites the base class define_preprocessor_flags_step.
        It adds the required preprocesser defines (including path-specific
        ones) for LFRic_atm.
        """
        super().define_preprocessor_flags_step()

        self.add_preprocessor_flags(
            ['-DUM_PHYSICS',
             '-DLFRIC',
             '-DUSSPPREC_32B',
             '-DLSPREC_32B',])

        path_flags = [AddFlags(match="$source/science/jules/*",
                               flags=['-DUM_JULES', '-I$output']),
                      AddFlags(match="$source/science/shumlib/*",
                               flags=['-I$output',
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
        This method adds shumlib to the lfric_base class
        get_linker_flags return.

        :returns: list of flags for the linker.
        '''
        libs = ['shumlib', ]
        return libs + super().get_linker_flags()

    def grab_files_step(self) -> None:
        """
        This method overwrites the base class grab_files_step. It includes
        all source files required for LFRic_atm.
        """
        super().grab_files_step()
        dirs = ['applications/lfric_atm/source',
                'science/gungho/source',
                'science/physics_schemes/source',
                'science/shared/source/',
                'interfaces/coupled_interface/source/',
                'interfaces/jules_interface/source/',
                'interfaces/physics_schemes_interface/source/',
                'interfaces/socrates_interface/source/',
                ]
        for directory in dirs:
            grab_folder(self.config,
                        src=self._lfric_apps_root / directory,
                        dst_label='')

        gr = GetRevision("../../dependencies.yaml")
        for repo in gr.keys():
            if repo == "lfric_apps":
                # For now don't support checking out the apps repo
                continue
            if repo == "lfric_core":
                # We don't support checking out lfric core, it will
                # be taken from an already checked out directory
                continue
            logger.info(f"Extracting '{repo}' from '{gr.get_source(repo)}' "
                        f" to 'science/{repo}', "
                        f"revision {gr.get_ref(repo)}")
            try:
                git_checkout(self.config,
                             gr.get_source(repo),
                             dst_label=f'science/{repo}',
                             revision=gr.get_ref(repo))
            except RuntimeError as error:
                logger.error(f"Cannot checkout '{repo}' from "
                             f"'{gr.get_source(repo)}' revision "
                             f"'{gr.get_ref(repo)}': {error}. ")
                sys.exit(-1)

        # Copy the optimisation scripts into a separate directory
        grab_folder(self.config, src=self._this_root / 'optimisation',
                    dst_label='optimisation')

    def find_source_files_step(
            self,
            path_filters: Optional[Iterable[Union[Exclude, Include]]] = None
            ) -> None:
        """
        Based on $LFRIC_APPS_ROOT/build/extract/extract.cfg.
        """

        extract_list = [ExtractList(self._lfric_apps_root / "build" /
                                    "extract" / "extract.yaml")]

        socrates_extract_cfg = (self._lfric_apps_root / "interfaces" /
                                "socrates_interface" / "build" /
                                "extract.yaml")
        extract_list.append(ExtractList(socrates_extract_cfg))

        jules_extract_cfg = (self._lfric_apps_root / "interfaces" /
                             "jules_interface" / "build" /
                             "extract.yaml")
        extract_list.append(ExtractList(jules_extract_cfg))

        # The sources are checked out under the 'science' directory:
        science_root = self.config.source_root / 'science'
        new_path_filters = []
        for extract_cfg in extract_list:
            for section in extract_cfg.get_all_sections():
                in_ex_list = extract_cfg.get_include_exclude_list(
                    section, science_root / section)
                new_path_filters.extend(in_ex_list)
        if path_filters:
            new_path_filters.extend(path_filters)

        super().find_source_files_step(path_filters=new_path_filters)

    def get_rose_meta(self) -> Path:
        """
        :returns: The path to the rose meta data config file.
        """
        return (self._this_root / 'rose-meta' / 'lfric-lfric_atm' / 'HEAD' /
                'rose-meta.conf')

    def analyse_step(
            self,
            ignore_dependencies: Optional[Iterable[str]] = None,
            find_programs: bool = False) -> None:
        '''
        The method adds lfric_atm specific list of dependencies to ignore.
        This list of shumlib may be used by developers during debugging.

        :param ignore_dependencies: Third party Fortran module names in
            USE statements, 'DEPENDS ON' files and modules to be ignored.
        :param find_programs: if the analyse step should try to automatically
            find all program units to build.
        '''
        lfric_atm_ignore_dependencies = [
            'c_shum_byteswap.o', 'f_shum_is_nan_mod', 'f_shum_field_mod',
            'f_shum_is_inf_mod', 'f_shum_file_mod', 'f_shum_is_denormal_mod'
            ]
        if ignore_dependencies:
            lfric_atm_ignore_dependencies.extend(ignore_dependencies)
        super().analyse_step(
            ignore_dependencies=lfric_atm_ignore_dependencies,
            find_programs=find_programs)

    def compile_fortran_step(
            self,
            common_flags: Optional[List[str]] = None,
            path_flags: Optional[List[AddFlags]] = None
            ) -> None:
        """
        Query site-specific settings.
        # TODO can be replaced once #313 is in Fab.
        """
        fc = self.config.tool_box.get_tool(Category.FORTRAN_COMPILER)
        fc = cast(Compiler, fc)
        profile = self.config.profile
        new_path_flags = get_lfric_atm_compile_fortran_specific_flags(fc,
                                                                      profile)
        if path_flags:
            new_path_flags.extend(path_flags)
        super().compile_fortran_step(common_flags=common_flags,
                                     path_flags=new_path_flags)


# -----------------------------------------------------------------------------
if __name__ == '__main__':

    logger = logging.getLogger('fab')
    logger.setLevel(logging.DEBUG)
    fab_lfric_atm = FabLFRicAtm(name="lfric_atm")
    fab_lfric_atm.build()
