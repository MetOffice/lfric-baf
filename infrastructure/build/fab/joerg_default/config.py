#! /usr/bin/env python3

'''This module contains a setup for Joerg's laptop :)
'''

import argparse
from typing import cast

from fab.tools import Category, Linker, ToolRepository

from default.config import Config as DefaultConfig


class Config(DefaultConfig):
    '''This config class sets specific flags for Joerg's laptop :)
    It makes gnu the default suite, and adds support for Vernier.
    '''

    def __init__(self):
        super().__init__()
        tr = ToolRepository()
        tr.set_default_compiler_suite("gnu")

    def handle_command_line_options(self, args: argparse.Namespace):
        '''Called with the user's command line options. It checks if
        Vernier profiling is requested, and if so, adds the required
        include and linking flags.
        '''

        super().handle_command_line_options(args)
        if args.vernier:
            tr = ToolRepository()
            gfortran = tr.get_tool(Category.FORTRAN_COMPILER, "gfortran")
            gfortran.add_flags(
                ['-I', '/home/joerg/work/vernier/local/include'])
            linker = tr.get_tool(Category.LINKER, "linker-gfortran")
            linker = cast(Linker, linker)
            linker.add_lib_flags(
                "vernier", ["-L", "/home/joerg/work/vernier/local/lib",
                            "-lvernier_f",  "-lvernier_c",  "-lvernier"])
