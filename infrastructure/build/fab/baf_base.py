#!/usr/bin/env python3
# ##############################################################################
#  (c) Crown copyright Met Office. All rights reserved.
#  For further details please refer to the file COPYRIGHT
#  which you should have received as part of this distribution
# ##############################################################################

'''This is an OO basic interface to FAB. It allows typical applications to
only modify very few settings to have a working FAB build script.
'''

import argparse
from importlib import import_module
import logging
import os
import sys
from typing import List

from fab.build_config import BuildConfig
from fab.steps.analyse import analyse
from fab.steps.archive_objects import archive_objects
from fab.steps.c_pragma_injector import c_pragma_injector
from fab.steps.compile_c import compile_c
from fab.steps.compile_fortran import compile_fortran
from fab.steps.find_source_files import find_source_files
from fab.steps.link import link_exe
from fab.steps.preprocess import preprocess_c, preprocess_fortran
from fab.steps.grab.folder import grab_folder
from fab.tools import Category, ToolBox, ToolRepository


class BafBase:
    '''This is the base class for all FAB scripts.

    :param str name: the name to be used for the workspace. Note that
        the name of the compiler will be added to it.
    :param Optional[str] root_symbol:
    '''
    # pylint: disable=too-many-instance-attributes
    def __init__(self, name, root_symbol=None):
        self._logger = logging.getLogger('fab')
        self._site = None
        self._platform = None
        self._target = None
        # We have to determine the site-specific setup first, so that e.g.
        # new compilers can be added before command line options are handled
        # (which might request this new compiler). So first parse the command
        # line for --site and --platform only:
        self.define_site_platform_target()

        # Now that site, platform and target are defined, import any
        # site-specific settings
        self.site_specific_setup()

        # Define the tool box, which might be started to be filled
        # when handling command line options:
        self._tool_box = ToolBox()
        parser = self.define_command_line_options()
        self.handle_command_line_options(parser)

        if root_symbol:
            self._root_symbol = root_symbol
        else:
            self._root_symbol = name

        self._config = BuildConfig(tool_box=self._tool_box,
                                   project_label=f'{name}-$compiler',
                                   verbose=True,
                                   n_procs=16,
                                   mpi=self._args.mpi,
                                   openmp=self._args.openmp,
                                   two_stage=True,
                                   )
        self._preprocessor_flags = []
        self._compiler_flags = []

        if self._site_config:
            self._site_config.update_toolbox(self._config)

    @property
    def site(self):
        ''':returns: the site.'''
        return self._site

    @property
    def logger(self):
        ''':returns: the logging instance to use.'''
        return self._logger

    @property
    def platform(self):
        ''':returns: the platform.'''
        return self._platform

    @property
    def target(self):
        ''':returns: the target (="site-platform").'''
        return self._target

    @property
    def config(self):
        ''':returns: the FAB BuildConfig instance.
        :rtype: :py:class:`fab.BuildConfig`
        '''
        return self._config

    def define_site_platform_target(self):
        '''This method defines the attributes site, platform (and
        target=site-platform) based on the command line option --site
        and --platform (using $SITE and $PLATFORM as a default). If
        site or platform is missing and the corresponding environment
        variable is not set, 'default' will be used.
        '''

        # Use `argparser.parse_known_args` to just handle --site and
        # --platform. We also suppress help (all of which will be handled
        # later, including proper help messages)
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("--site", "-s", type=str, default="$SITE")
        parser.add_argument("--platform", "-p", type=str, default="$PLATFORM")

        args = parser.parse_known_args()[0]   # Ignore element [1]=unknown args
        if args.site == "$SITE":
            self._site = os.environ.get("SITE", "default")
        elif args.site:
            self._site = args.site
        else:
            self._site = "default"

        if args.platform == "$PLATFORM":
            self._platform = os.environ.get("PLATFORM", "default")
        elif args.platform:
            self._platform = args.platform
        else:
            self._platform = "default"

        # Define target attribute for site&platform-specific files
        # If none are specified, just use a single default (instead of
        # default-default)
        if self._platform == "default" and self._site == "default":
            self._target = "default"
        else:
            self._target = f"{self._site}_{self._platform}"

    def site_specific_setup(self):
        '''Imports a site-specific config file. The location is based
        on the attribute target (which is set to be site-platform).
        '''
        try:
            config_module = import_module(f"{self.target}.config")
        except ModuleNotFoundError:
            # We log a warning, but proceed, since there is no need to
            # have a site-specific file.
            self._logger.warning(f"Cannot find site-specific module "
                                 f"'{self.target}.config'.")
            self._site_config = None
            return
        self.logger.info(f"baf_base: Imported '{self.target}'")
        # The constructor handles everything.
        self._site_config = config_module.Config()

    def define_command_line_options(self, parser=None):
        '''Defines command line options. Can be overwritten by a derived
        class which can provide its own instance (to easily allow for a
        different description).
        :param parser: optional a pre-defined argument parser. If not, a
            new instance will be created.
        :type argparse: Optional[:py:class:`argparse.ArgumentParser`]
        '''

        if not parser:
            # The formatter class makes sure to print default settings
            parser = argparse.ArgumentParser(
                description=("A Baf-based build system. Note that if --suite "
                             "is specified, this will change the default for "
                             "compiler and linker"),
                formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        parser.add_argument(
            '--suite', '-v', type=str, default=None,
            help="Sets the default suite for compiler and linker")
        parser.add_argument(
            '--fc', '-fc', type=str, default="$FC",
            help="Name of the Fortran compiler to use")
        parser.add_argument(
            '--cc', '-cc', type=str, default="$CC",
            help="Name of the C compiler to use")
        parser.add_argument(
            '--ld', '-ld', type=str, default="$LD",
            help="Name of the linker to use")
        parser.add_argument(
            '--mpi', '-mpi', default=True, action="store_true",
            help="Enable MPI")
        parser.add_argument(
            '--no-mpi', '-no-mpi', action="store_false",
            dest="mpi", help="Disable MPI")
        parser.add_argument(
            '--openmp', '-openmp', default=True, action="store_true",
            help="Enable OpenMP")
        parser.add_argument(
            '--no-openmp', '-no-openmp', action="store_false",
            dest="openmp", help="Disable OpenMP")
        parser.add_argument("--site", "-s", type=str,
                            default="$SITE or 'default'",
                            help="Name of the site to use.")
        parser.add_argument("--platform", "-p", type=str,
                            default="$PLATFORM or 'default'",
                            help="Name of the platform of the site to use.")
        return parser

    def handle_command_line_options(self, parser):
        '''Analyse the actual command line options using the specified parser.
        The base implementation will handle the `--suite` parameter, and
        compiler/linker parameters (including the usage of environment
        variables). Needs to be overwritten to handle additional options
        specified by a derived script.

        :param parser: the argument parser.
        :type parser: :py:class:`argparse.ArgumentParser`
        '''
        # pylint: disable=too-many-branches
        self._args = parser.parse_args(sys.argv[1:])

        tr = ToolRepository()
        if self._args.suite:
            tr.set_default_compiler_suite(self._args.suite)

            self.logger.info(f"Setting suite to '{self._args.suite}'.")
            # suite will overwrite use of env variables, so change the
            # value of these arguments to be none so they will be ignored
            if self._args.fc == "$FC":
                self._args.fc = None
            if self._args.cc == "$CC":
                self._args.cc = None
            if self._args.ld == "$LD":
                self._args.ld = None
        else:
            # If no suite is specified, if required set the defaults
            # for compilers based on the environment variables.
            if self._args.fc == "$FC":
                self._args.fc = os.environ.get("FC")
            if self._args.cc == "$CC":
                self._args.cc = os.environ.get("CC")
            if self._args.ld == "$LD":
                self._args.ld = os.environ.get("LD")

        # If no suite was specified, and a special tool was requested,
        # add it to the tool box:
        if self._args.cc:
            cc = tr.get_tool(Category.C_COMPILER, self._args.cc)
            self._tool_box.add_tool(cc)
        if self._args.fc:
            fc = tr.get_tool(Category.FORTRAN_COMPILER, self._args.fc)
            self._tool_box.add_tool(fc)
        if self._args.ld:
            ld = tr.get_tool(Category.LINKER, self._args.ld)
            self._tool_box.add_tool(ld)

    def define_preprocessor_flags(self):
        '''Top level function that sets preprocessor flags
        by calling self.set_flags
        '''
        preprocessor_flags = []
        self.set_flags(preprocessor_flags, self._preprocessor_flags)

    def define_compiler_flags(self):
        '''Top level function that sets (compiler- and site-specific)
        compiler flags by calling self.set_flags
        '''
        compiler = self._tool_box.get_tool(Category.FORTRAN_COMPILER,
                                           mpi=self.config.mpi)

        if compiler.suite == "intel-classic":

            debug_flags = ['-g', '-traceback']
            compiler_flags = debug_flags

            self.set_flags(compiler_flags, self._compiler_flags)

        elif compiler.suite in ["gnu"]:

            debug_flags = ['-g']
            compiler_flags = debug_flags

            self.set_flags(compiler_flags, self._compiler_flags)

        else:
            raise RuntimeError(f"Unknown compiler suite '{compiler.suite}'.")

        return compiler

    def get_linker_flags(self) -> List[str]:
        '''Base class for setting linker flags. This base implementation
        for now just returns an empty list

        :returns: list of flags for the linker.
        '''
        return []

    def set_flags(self, list_of_flags, flag_group):
        for flag in list_of_flags:
            if flag not in flag_group:
                flag_group.append(flag)

    def grab_files(self):
        grab_folder(self.config, src="", dst_label="")

    def find_source_files(self):
        find_source_files(self.config)

    def preprocess_c(self, path_flags=None):
        preprocess_c(self.config, common_flags=self._preprocessor_flags,
                     path_flags=path_flags)

    def preprocess_fortran(self, path_flags=None):
        preprocess_fortran(self.config, common_flags=self._preprocessor_flags,
                           path_flags=path_flags)

    def analyse(self):
        analyse(self.config, root_symbol=self._root_symbol)

    def compile_c(self):
        compile_c(self.config)

    def compile_fortran(self, path_flags=None):
        compile_fortran(self.config, common_flags=self._compiler_flags,
                        path_flags=path_flags)

    def archive_objects(self):
        archive_objects(self.config)

    def link(self):
        link_exe(self.config, libs=self.get_linker_flags())

    def build(self):
        # We need to use with to trigger the entrance/exit functionality,
        # but otherwise the config object is used from this object, so no
        # need to use it anywhere.
        with self._config as _:
            self.grab_files()
            self.find_source_files()
            c_pragma_injector(self.config)
            self.define_preprocessor_flags()
            self.preprocess_c()
            self.preprocess_fortran()
            self.analyse()
            self.define_compiler_flags()
            self.compile_c()
            self.compile_fortran()
            # Disable archiving due to
            # https://github.com/MetOffice/fab/issues/310
            # Archives can contain several versions of a file (with different)
            # hashes, meaning at link time an older version might be used,
            # even if a newer one is available.
            # self.archive_objects()
            self.link()


# ==========================================================================
if __name__ == "__main__":

    logger = logging.getLogger('fab')
    logger.setLevel(logging.DEBUG)
    baf_base = BafBase(name="command-line-test",
                       root_symbol=None)
