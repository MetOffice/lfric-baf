#! /usr/bin/env python3

'''
This module contains a setup for Joerg's laptop :)
'''

import argparse
from typing import cast, List

from fab.build_config import BuildConfig
from fab.tools import Category, Linker, ToolRepository

from default.config import Config as DefaultConfig


class Config(DefaultConfig):
    '''
    This config class sets specific flags for Joerg's laptop :)
    It makes gnu the default suite, and adds support for Vernier.
    '''

    def __init__(self):
        super().__init__()
        tr = ToolRepository()
        tr.set_default_compiler_suite("gnu")

    def get_valid_profiles(self) -> List[str]:
        '''
        Determines the list of all allowed compiler profiles. Here we
        add one additional profile `memory-debug`. Note that the default
        setup will automatically create that mode for any available compiler.

        :returns List[str]: list of all supported compiler profiles.
        '''
        return super().get_valid_profiles() + ["memory-debug"]

    def update_toolbox(self, build_config: BuildConfig) -> None:
        '''
        Define additional profiling mode 'memory-debug'.

        :param build_config: the Fab build configuration instance
        :type build_config: :py:class:`fab.BuildConfig`
        '''

        # The base class needs to be called first to create all standard
        # profile modes:
        super().update_toolbox(build_config)

        tr = ToolRepository()
        gfortran = tr.get_tool(Category.FORTRAN_COMPILER, "gfortran")
        linker = tr.get_tool(Category.LINKER, "linker-gfortran")
        # Define the new compilation profile `memory-debug`
        gfortran.add_flags(["-fsanitize=address"], "memory-debug")
        linker.add_post_lib_flags(["-static-libasan"], "memory-debug")

    def handle_command_line_options(self, args: argparse.Namespace) -> None:
        '''
        Called with the user's command line options. It checks if
        Vernier profiling is requested, and if so, adds the required
        include and linking flags.

        :param argparse.Namespace args: the command line options added in
            the site configs
        '''

        super().handle_command_line_options(args)

        if args.vernier:
            tr = ToolRepository()
            gfortran = tr.get_tool(Category.FORTRAN_COMPILER, "gfortran")
            gfortran.add_flags(
                ['-I', '/home/joerg/work/Vernier/local/include'], "base")
            linker = tr.get_tool(Category.LINKER, "linker-gfortran")
            linker = cast(Linker, linker)

            # Add setting for Vernier
            linker.add_lib_flags(
                "vernier", ["-L", "/home/joerg/work/Vernier/local/lib",
                            "-lvernier_f",  "-lvernier_c",  "-lvernier"])
