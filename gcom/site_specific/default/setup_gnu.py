#!/usr/bin/env python3

'''This file contains a function that sets the default flags for all
GNU based compilers in the ToolRepository.

This function gets called from the default site-specific config file
'''

import argparse

from typing import cast
from fab.build_config import BuildConfig
from fab.tools import Category, Linker, ToolRepository


def setup_gnu(build_config: BuildConfig, args: argparse.Namespace):
    # pylint: disable=unused-argument
    '''Defines the default flags for all GNU compilers.

    :para build_config: the build config from which required parameters
        can be taken.
    :param args: all command line options
    '''

    tr = ToolRepository()
    gfortran = tr.get_tool(Category.FORTRAN_COMPILER, "gfortran")

    if not gfortran.is_available:
        return

    # The base flags
    # ==============
    gfortran.add_flags(
        ['-ffree-line-length-none', '-Wall',
         '-g',
         '-fallow-argument-mismatch',
         '-Werror=unused-value',
         '-Werror=tabs',
         '-std=f2008',
         ],
        "base")

    runtime = ["-fcheck=all", "-ffpe-trap=invalid,zero,overflow"]
    init = ["-finit-integer=31173",  "-finit-real=snan",
            "-finit-logical=true", "-finit-character=85"]
    # Full debug
    # ==========
    gfortran.add_flags(runtime + ["-O0"] + init, "full-debug")

    # Fast debug
    # ==========
    gfortran.add_flags(runtime + ["-Og"], "fast-debug")

    # Production
    # ==========
    gfortran.add_flags(["-Ofast"], "production")

    # unit-tests
    # ==========
    gfortran.add_flags(runtime + ["-O0"] + init, "unit-tests")
