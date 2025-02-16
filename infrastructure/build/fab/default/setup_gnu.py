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
    pf = gfortran.profile_flags
    # Already defined atm:
    # pf.define_profile("default")
    pf.define_profile("full-debug", "default")
    pf.define_profile("fast-debug", "default")
    pf.define_profile("production", "default")
    pf.define_profile("unit-tests", "default")

    pf.add_flags("default", ['-ffree-line-length-none', '-Wall',
                             '-g', "-Werror=conversion",
                             '-Werror=character-truncation',
                             '-Werror=unused-value',
                             '-Werror=tabs',
                             '-std=f2008',
                             '-fdefault-real-8',
                             '-fdefault-double-8',
                             ])
    runtime = ["-fcheck=all", "-ffpe-trap=invalid,zero,overflow"]
    init = ["-finit-integer=31173",  "-finit-real=snan",
            "-finit-logical=true", "-finit-character=85"]
    pf.add_flags("full-debug", runtime + ["-O0"] + init)
    pf.add_flags("unit-tests", runtime + ["-O0"] + init)
    pf.add_flags("fast-debug", runtime + ["-Og"])
    pf.add_flags("production", ["-Ofast"])

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
