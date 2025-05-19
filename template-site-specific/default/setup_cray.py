#!/usr/bin/env python3

'''This file contains a function that sets the default flags for the Cray
compilers in the ToolRepository.

This function gets called from the default site-specific config file
'''

import argparse
from typing import cast

from fab.build_config import BuildConfig
from fab.tools import Category, Compiler, Linker, ToolRepository


def setup_cray(build_config: BuildConfig, args: argparse.Namespace):
    # pylint: disable=unused-argument
    '''Defines the default flags for ftn.

    :param build_config: the build config from which required parameters
        can be taken.
    :param args: all command line options
    '''

    tr = ToolRepository()
    ftn = tr.get_tool(Category.FORTRAN_COMPILER, "crayftn-ftn")
    ftn = cast(Compiler, ftn)

    if not ftn.is_available:
        return

    # The base flags
    # ==============
    flags = ["-g", "-G0", "-m", "0",    # 
             "-ef",                     # use lowercase module names!Important!
             "-hnocaf",                 # Required for linking with C++
             ]


    # Full debug
    # ==========
    ftn.add_flags(["-Ktrap=fp",    # floating point checking
                   "-R", "bcdps",  # bounds, array shape, collapse,
                                   # pointer, string checking
                   "-O0"],         # No optimisation
                  "full-debug")
    if ftn.get_version() >= (15, 0):
        ftn.add_flags(["-G0"], "full-debug")
    else:
        ftn.add_flags(["-Gfast"], "full-debug")

    # Fast debug
    # ==========
    ftn.add_flags(["-O2"], "fast-debug")
    if ftn.get_version() >= (15, 0):
        ftn.add_flags(["-G2"], "fast-debug")
    else:
        ftn.add_flags(["-Gfast"], "fast-debug")

    # Production
    # ==========
    ftn.add_flags(["-O3"], "production")

    # Set up the linker
    # =================
    linker = tr.get_tool(Category.LINKER, f"linker-{ftn.name}")
    linker = cast(Linker, linker)

    # Setup library info, e.g.:
    # linker.add_lib_flags("yaxt", ["-L/some/path", "-lyaxt", "-lyaxt_c"])
    
    # Add more flags to be always used, e.g.:
    # linker.add_post_lib_flags("-lcraystdc++")

    # Using the GNU compiler on Crays for now needs the additional
    # flag -fallow-argument-mismatch to compile certain mpi codes.
    # You can use:
    # ftn = tr.get_tool(Category.FORTRAN_COMPILER, "crayftn-gfortran")
    # ftn.add_flags("-fallow-argument-mismatch")
