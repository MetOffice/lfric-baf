#!/usr/bin/env python3
# ##############################################################################
#  (c) Crown copyright Met Office. All rights reserved.
#  For further details please refer to the file COPYRIGHT
#  which you should have received as part of this distribution
# ##############################################################################

'''
This is an OO basic interface to FAB. It allows the typical LFRic
applications to only modify very few settings to have a working FAB build
script.
'''

import argparse
import inspect
import logging
import os
from pathlib import Path
from typing import List, Optional, Iterable, Union

from fab.artefacts import ArtefactSet, SuffixFilter
from fab.build_config import BuildConfig
from fab.steps.analyse import analyse
from fab.steps.find_source_files import Exclude, Include
from fab.steps.psyclone import psyclone, preprocess_x90
from fab.steps.grab.folder import grab_folder
from fab.tools import Category
from fab.util import input_to_output_fpath

from baf_base import BafBase
from lfric_common import configurator
from rose_picker_tool import get_rose_picker
from templaterator import Templaterator


class LFRicBase(BafBase):
    '''
    This is the base class for all LFRic FAB scripts.

    :param str name: the name to be used for the workspace. Note that
        the name of the compiler will be added to it.
    :param root_symbol: the name of the main program. Defaults to `name`
        if not specified.

    '''
    # pylint: disable=too-many-instance-attributes
    def __init__(self, name: str, root_symbol: Optional[str] = None):

        super().__init__(name)
        # If the user wants to overwrite the default root symbol (which
        # is `name`):
        if root_symbol:
            self.set_root_symbol(root_symbol)

        this_file = Path(__file__)
        # The root directory of the LFRic Core
        self._lfric_core_root = this_file.parents[3]

        # We need to find the apps directory (it will be required when
        # finding source files in the build scripts). We shouldn't assume
        # that it is 'next' to the core directory, nor should we assume
        # that the name is 'apps'. In order to avoid reliance on any
        # environment variable, we analyse the call tree to find the first
        # call that is not in our parent directory (in case that we ever
        # add another layer of base class).
        my_base_dir = this_file.parent
        for caller in inspect.stack():
            abs_path_caller = Path(caller[1])
            if not my_base_dir.samefile(abs_path_caller.parent):
                self.logger.debug(f"lfric_base: found caller: {caller[1]}")
                self._lfric_apps_root = self.get_apps_root_dir(abs_path_caller)
                break
            self.logger.debug(f"lfric_base: searching caller: {caller[1]}")
        else:
            # All callers are in this directory? Issue warning, and assume
            # that lfric_apps is 'next' to lfric_core
            self._lfric_apps_root = self.lfric_core_root.parent / 'apps'
            self.logger.warning(f"Could not find apps directory, defaulting "
                                f"to '{self._lfric_apps_root}'.")

        self._psyclone_config = (self.config.source_root / 'psyclone_config' /
                                 'psyclone.cfg')

    def get_apps_root_dir(self, path: Path) -> Path:
        '''
        This identifies the root directory of the LFRic apps directory,
        given a file in the apps directory. This is done by looking for a
        file `dependencies.sh` in the directory, and searching up in the
        directory tree till it is found.

        param path: the path to a file in the apps directory.
        '''
        dep_name = "dependencies.sh"
        # path.anchor gives us the root as string:
        while path.anchor != str(path) and not (path/dep_name).exists():
            self.logger.debug(f"lfric_base: no '{dep_name}' in '{path}'.")
            path = path.parent
        # If we found the file, return the path
        if path.anchor != str(path):
            self.logger.info(f"lfric_base: lfric_apps dir = '{path}'.")
            return path

        # It is possible that we are building an application in the core
        # repository, so to support this we use the core root also
        # as the apps root:
        return self._lfric_core_root

    def define_command_line_options(
            self,
            parser: Optional[argparse.ArgumentParser] = None
            ) -> argparse.ArgumentParser:
        '''
        This adds LFRic specific command line options to the base class
        define_command_line_option. Currently, --rose_piker, --vernier
        and --precision options are added.

        :param parser: optional a pre-defined argument parser.
        :returns: the argument parser with the LFRic specific options added.
        '''
        parser = super().define_command_line_options()

        parser.add_argument(
            '--rose_picker', '-rp', type=str, default="system",
            help="Version of rose_picker. Use 'system' to use an installed "
                 "version.")
        parser.add_argument("--vernier", action="store_true", default=False,
                            help="Support profiling with Vernier.")
        parser.add_argument(
            '--precision', '-pre', type=str, default=None,
            help="Precision for reals, choose from '64', '32', \
                default is R_SOLVER_PRECISION=32 while others are 64")
        return parser

    @property
    def lfric_core_root(self) -> Path:
        '''
        :returns: the root directory of the LFRic core repository.
        :rtype: Path
        '''
        return self._lfric_core_root

    @property
    def lfric_apps_root(self) -> Path:
        '''
        :returns: the root directory of the LFRic apps repository.
        :rtype: Path
        '''
        return self._lfric_apps_root

    def define_preprocessor_flags_step(self) -> None:
        '''
        This method overwrites the base class define_preprocessor_flags.
        It uses add_preprocessor_flags to set up preprocessing flags for LFRic
        applications. Currently, the precision flags with precision level set
        in the command line option and the '-DUSE_XIOS' flag are set here.
        '''
        if self.args.precision:
            precision_flags = ['-DRDEF_PRECISION=' + self.args.precision,
                               '-DR_SOLVER_PRECISION=' + self.args.precision,
                               '-DR_TRAN_PRECISION=' + self.args.precision,
                               '-DR_BL_PRECISION=' + self.args.precision]
        else:
            precision_flags = []
            r_def_precision = os.environ.get("RDEF_PRECISION")
            r_solver_precision = os.environ.get("R_SOLVER_PRECISION")
            r_tran_precision = os.environ.get("R_TRAN_PRECISION")
            r_bl_precision = os.environ.get("R_BL_PRECISION")

            if r_def_precision:
                precision_flags += ['-DRDEF_PRECISION='+r_def_precision]
            else:
                precision_flags += ['-DRDEF_PRECISION=64']

            if r_solver_precision:
                precision_flags += ['-DR_SOLVER_PRECISION='+r_solver_precision]
            else:
                precision_flags += ['-DR_SOLVER_PRECISION=32']

            if r_tran_precision:
                precision_flags += ['-DR_TRAN_PRECISION='+r_tran_precision]
            else:
                precision_flags += ['-DR_TRAN_PRECISION=64']

            if r_bl_precision:
                precision_flags += ['-DR_BL_PRECISION='+r_bl_precision]
            else:
                precision_flags += ['-DR_BL_PRECISION=64']

        # build/tests.mk - for mpi unit tests, not used atm
        mpi_tests_flags = ['-DUSE_MPI=YES']

        self.add_preprocessor_flags(precision_flags+['-DUSE_XIOS'])
        # -DUSE_XIOS is not found in makefile but in fab run_config and
        # driver_io_mod.F90

    def get_linker_flags(self) -> List[str]:
        '''
        This method overwrites the base class get_liner_flags. It passes the
        libraries that LFRic uses to the linker. Currently, these libraries
        include yaxt, xios, netcdf, hdf5 and vernier

        :returns: list of flags for the linker.
        :rtype: List[str]
        '''
        libs = ['yaxt', 'xios', 'netcdf', 'hdf5']
        if self.args.vernier:
            libs.append("vernier")
        return libs + super().get_linker_flags()

    def grab_files_step(self) -> None:
        '''
        This method overwrites the base class grab_files_step. It includes all
        the LFRic core directories that are commonly required for building
        LFRic applications. It also grabs the psydata directory for profiling,
        if required.
        '''
        dirs = ['infrastructure/source/',
                'components/driver/source/',
                'components/inventory/source/',
                'components/science/source/',
                'components/lfric-xios/source/',
                'components/coupling/source/',
                ]

        # pylint: disable=redefined-builtin
        for dir in dirs:
            grab_folder(self.config, src=self.lfric_core_root / dir,
                        dst_label='')

        # Copy the PSyclone Config file into a separate directory
        dir = "etc"
        grab_folder(self.config, src=self.lfric_core_root / dir,
                    dst_label='psyclone_config')

        compiler = self.config.tool_box[Category.FORTRAN_COMPILER]
        linker = self.config.tool_box.get_tool(Category.LINKER,
                                               mpi=self.config.mpi,
                                               openmp=self.config.openmp)
        if (self.args.vernier or
                "tau_f90.sh" in [compiler.exec_name, linker.exec_name]):
            # Profiling. Grab the required psydata directory as well:
            if self.args.vernier:
                try:
                    linker.get_lib_flags("vernier")
                except RuntimeError:
                    raise RuntimeError(f"The linker{linker} does not have "
                                       f"linker flags for Vernier.")
                dir = "vernier"

            else:
                dir = "tau"
            grab_folder(self.config, src=self.lfric_core_root /
                        "infrastructure" / "build" / "psyclone" / "psydata"
                        / dir, dst_label='psydata')

    def find_source_files_step(
            self,
            path_filters: Optional[Iterable[Union[Exclude, Include]]] = None
            ) -> None:
        '''
        This method overwrites the base class find_source_files_step.
        It first calls the configurator_step to set up the configurator.
        Then it finds all the source files in the LFRic core directories,
        excluding the unit tests. Finally, it calls the templaterator_step.

        :param path_filters: optional list of path filters to be passed to
            Fab find_source_files, default is None.
        :type path_filters: Optional[Iterable[Exclude, Include]]
        '''
        self.configurator_step()

        if path_filters is None:
            path_filters = []
        path_filters.append(Exclude('unit-test', '/test/'))
        super().find_source_files_step(path_filters=path_filters)

        self.templaterator_step(self.config)

    def configurator_step(self) -> None:
        '''
        This method first gets the rose meta data information by calling
        get_rose_meta. If the rose meta data is available, it then get the
        rose picker tool by calling the get_rose_picker. Finally, it runs
        the LFRic configurator with the LFRic core and apps sources by calling
        configurator.
        '''
        rose_meta = self.get_rose_meta()
        if rose_meta:
            # Get the right version of rose-picker, depending on
            # command line option (defaulting to v2.0.0)
            # TODO: Ideally we would just put this into the toolbox,
            # but atm we can't put several tools of one category in
            # (so ToolBox will need to support more than one MISC tool)
            rp = get_rose_picker(self.args.rose_picker)
            # Ideally we would want to get all source files created in
            # the build directory, but then we need to know the list of
            # files to add them to the list of files to process
            configurator(self.config, lfric_core_source=self.lfric_core_root,
                         lfric_apps_source=self.lfric_apps_root,
                         rose_meta_conf=rose_meta,
                         rose_picker=rp)

    def templaterator_step(self, config: BuildConfig) -> None:
        '''
        This method runs the LFRic templaterator Fab tool.

        :param config: the Fab build configuration
        :type config: :py:class:`fab.BuildConfig`
        '''
        base_dir = self.lfric_core_root / "infrastructure" / "build" / "tools"

        templaterator = Templaterator(base_dir/"Templaterator")
        config.artefact_store["template_files"] = set()
        t90_filter = SuffixFilter(ArtefactSet.INITIAL_SOURCE, [".t90", ".T90"])
        template_files = t90_filter(config.artefact_store)
        # Don't bother with parallelising this, atm there is only one file:
        for template_file in template_files:
            out_dir = input_to_output_fpath(config=config,
                                            input_path=template_file).parent
            out_dir.mkdir(parents=True, exist_ok=True)
            templ_r32 = {"kind": "real32", "type": "real"}
            templ_r64 = {"kind": "real64", "type": "real"}
            templ_i32 = {"kind": "int32", "type": "integer"}
            for key_values in [templ_r32, templ_r64, templ_i32]:
                out_file = out_dir / f"field_{key_values['kind']}_mod.f90"
                templaterator.run(template_file, out_file,
                                  key_values=key_values)
                config.artefact_store.add(ArtefactSet.FORTRAN_BUILD_FILES,
                                          out_file)

    def get_rose_meta(self) -> Union[Path, None]:
        '''
        This method returns the path to the rose meta data config file.
        Currently, it returns none for the LFRic applications to overwrite
        if required.
        '''
        return None

    def analyse_step(self) -> None:
        '''
        The method overwrites the base class analyse_step.
        For LFRic, it first runs the preprocess_x90_step and then runs
        psyclone_step. Finally, it calls Fab's analyse for dependency
        analysis, ignoring the third party modules that are commonly
        used by LFRic.
        '''
        self.preprocess_x90_step()
        self.psyclone_step()
        analyse(self.config, root_symbol=self.root_symbol,
                ignore_mod_deps=['netcdf', 'MPI', 'yaxt', 'pfunit_mod',
                                 'xios', 'mod_wait'])

    def preprocess_x90_step(self) -> None:
        """
        Invokes the Fab preprocess step for all X90 files.
        """
        # TODO: Fab does not support path-specific flags for X90 files.
        preprocess_x90(self.config,
                       common_flags=self.preprocess_flags_common)

    def psyclone_step(self) -> None:
        '''
        This method runs Fab's psyclone. It first sets the additional psyclone
        command line arguments by calling get_psyclone_config to get the
        PSyclone configuration file and by calling
        `get_additional_psyclone_options` to get additional psyclone command
        line set by the user, e.g. for profiling, if any. Finally, Fab's
        psyclone is called with the Fab build configuration, the kernel root
        directory, the transforamtion script got through calling
        `get_transformation_script`, the api, and the additional psyclone
        command line arguments.
        '''
        psyclone_cli_args = self.get_psyclone_config()
        psyclone_cli_args.extend(self.get_additional_psyclone_options())

        psyclone(self.config, kernel_roots=[self.config.build_output],
                 transformation_script=self.get_transformation_script,
                 api="dynamo0.3",
                 cli_args=psyclone_cli_args)

    def get_psyclone_config(self) -> List[str]:
        '''
        :returns: the command line options to pick the right
            PSyclone config file.
        :rtype: List[str]
        '''
        return ["--config", self._psyclone_config]

    def get_additional_psyclone_options(self) -> List[str]:
        '''
        :returns: Additional PSyclone command line options. This
            basic version checks if profiling using Tau or Vernier is enabled,
            and if so, adds the kernel profiling flags to PSyclone.
        :rtype: List[str]
        '''
        compiler = self.config.tool_box[Category.FORTRAN_COMPILER]
        linker = self.config.tool_box.get_tool(Category.LINKER,
                                               mpi=self.config.mpi)
        if (self.args.vernier or
                "tau_f90.sh" in [compiler.exec_name, linker.exec_name]):
            return ["--profile", "kernels"]
        return []

    def get_transformation_script(self, fpath: Path,
                                  config: BuildConfig) -> Path:
        '''
        This method returns the path to the transformation script that PSyclone
        will use for each x90 file. It first checks if there is a specific
        transformation script for the x90 file. If not, it will see whether a
        global transformation script can be used.

        :param fpath: the path to the file being processed.
        :param config: the FAB BuildConfig instance.
        :returns: the transformation script to be used by PSyclone.
        '''
        # Newer LFRic versions have a psykal directory
        optimisation_path = (config.source_root / "optimisation" /
                             f"{self.site}-{self.platform}" / "psykal")
        if not optimisation_path.exists():
            optimisation_path = (config.source_root / "optimisation" /
                                 f"{self.site}-{self.platform}")
        relative_path = None
        for base_path in [config.source_root, config.build_output]:
            try:
                relative_path = fpath.relative_to(base_path)
            except ValueError:
                pass
        if relative_path:
            local_transformation_script = (optimisation_path /
                                           (relative_path.with_suffix('.py')))
            if local_transformation_script.exists():
                return local_transformation_script

        global_transformation_script = optimisation_path / 'global.py'
        if global_transformation_script.exists():
            return global_transformation_script
        return ""


# ==========================================================================
if __name__ == "__main__":
    # This tests the LFRicBase class using the command line.
    logger = logging.getLogger('fab')
    logger.setLevel(logging.DEBUG)
    lfric_base = LFRicBase(name="command-line-test")
