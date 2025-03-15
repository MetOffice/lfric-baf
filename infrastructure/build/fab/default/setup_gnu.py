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
    gfortran.add_flags(['-ffree-line-length-none', '-Wall',
                  '-g', "-Werror=conversion",
                  '-Werror=character-truncation',
                  '-Werror=unused-value',
                  '-Werror=tabs',
                  '-std=f2008',
                  '-fdefault-real-8',
                  '-fdefault-double-8',
                  ],
                  "base", )
    runtime = ["-fcheck=all", "-ffpe-trap=invalid,zero,overflow"]
    init = ["-finit-integer=31173",  "-finit-real=snan",
            "-finit-logical=true", "-finit-character=85"]
    gfortran.add_flags(runtime + ["-O0"] + init, "full-debug")
    gfortran.add_flags(runtime + ["-O0"] + init, "unit-tests")
    gfortran.add_flags(runtime + ["-Og"],        "fast-debug")
    gfortran.add_flags(["-Ofast"],               "production")

    # ATM we don't use a shell when running a tool, and as such
    # we can't directly use "$()" as parameter. So query these values using
    # Fab's shell tool (doesn't really matter which shell we get, so just
    # ask for the default):
    shell = tr.get_default(Category.SHELL)

    try:
        # We must remove the trailing new line, and create a list:
        nc_flibs = shell.run(additional_parameters=["-c", "nf-config --flibs"],
                             capture_output=True).strip().split()
    except RuntimeError:
        nc_flibs = []

    # This will implicitly affect all gfortran based linkers, e.g.
    # linker-mpif90-gfortran will use these flags as well.
    linker = tr.get_tool(Category.LINKER, "linker-gfortran")
    linker = cast(Linker, linker)
    linker.add_lib_flags("netcdf", nc_flibs)
    linker.add_lib_flags("yaxt", ["-lyaxt", "-lyaxt_c"])
    linker.add_lib_flags("xios", ["-lxios"])
    linker.add_lib_flags("hdf5", ["-lhdf5"])

    # Always link with C++ libs
    linker.add_post_lib_flags(["-lstdc++"])
