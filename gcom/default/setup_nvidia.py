#!/usr/bin/env python3

'''This file contains a function that sets the default flags for the NVIDIA
compilers in the ToolRepository.

This function gets called from the default site-specific config file
'''

import argparse
from typing import cast

from fab.build_config import BuildConfig
from fab.tools import Category, Compiler, Linker, ToolRepository


def setup_nvidia(build_config: BuildConfig, args: argparse.Namespace):
    # pylint: disable=unused-argument
    '''Defines the default flags for nvfortran.

    :param build_config: the build config from which required parameters
        can be taken.
    :param args: all command line options
    '''

    tr = ToolRepository()
    nvfortran = tr.get_tool(Category.FORTRAN_COMPILER, "nvfortran")
    nvfortran = cast(Compiler, nvfortran)

    if not nvfortran.is_available:
        return

    # The base flags
    # ==============
    flags = ["-Mextend",           # 132 characters line length
             "-g", "-traceback",
             "-r8",                # Default 8 bytes reals
             "-O0",                # No optimisations
             ]

    lib_flags = ["-c++libs"]

    # Handle accelerator options:
    if args.openacc or args.openmp:
        host = args.host.lower()
    else:
        # Neither openacc nor openmp specified
        host = ""

    if args.openacc:
        if host == "gpu":
            flags.extend(["-acc=gpu", "-gpu=managed"])
            lib_flags.extend(["-aclibs", "-cuda"])
        else:
            # CPU
            flags.extend(["-acc=cpu"])
    elif args.openmp:
        if host == "gpu":
            flags.extend(["-mp=gpu", "-gpu=managed"])
            lib_flags.append("-cuda")
        else:
            # OpenMP on CPU, that's already handled by Fab
            pass

    nvfortran.add_flags(flags, "base")

    # Full debug
    # ==========
    nvfortran.add_flags(["-O0", "-fp-model=strict"], "full-debug")

    # Fast debug
    # ==========
    nvfortran.add_flags(["-O2", "-fp-model=strict"], "fast-debug")

    # Production
    # ==========
    nvfortran.add_flags(["-O4"], "production")
