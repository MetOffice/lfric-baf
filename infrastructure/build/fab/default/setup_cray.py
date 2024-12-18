#!/usr/bin/env python3

'''This file contains a function that sets the default flags for all
GNU based compilers in the ToolRepository.

This function gets called from the default site-specific config file
'''

from fab.build_config import BuildConfig
from fab.tools import Category, Tool, ToolRepository


def setup_gnu(build_config: BuildConfig):
    '''Defines the default flags for all Cray compilers.

    :para build_config: the build config from which required parameters
        can be taken.
    '''

    tr = ToolRepository()
    gfortran = tr.get_tool(Category.FORTRAN_COMPILER, "gfortran")
    flags = ['-ffree-line-length-none', '-g',
             '-Werror=character-truncation', '-Werror=unused-value',
             '-Werror=tabs', '-fdefault-real-8', '-fdefault-double-8',
             '-Ditworks'
             ]
    gfortran.add_flags(flags)

    # ATM a linker is not using a compiler wrapper, and so
    # linker-mpif90-gfortran does not inherit from linker-gfortran.
    # For now set the flags in both linkers:

    # ATM we don't use a shell when starting a tool, and as such
    # we can't directly use "$()". So query these values using
    # a shell tool:
    shell = tr.get_default(Category.SHELL)
    # We must remove the trailing new line, and create a list:
    nc_flibs = shell.run(additional_parameters=["nf-config --flibs"],
                         capture_output=True).strip().split()

    for linker_name in ["linker-gfortran", "linker-mpif90-gfortran"]:
        linker = tr.get_tool(Category.LINKER, linker_name)

        linker.add_lib_flags("netcdf", nc_flibs, silent_replace=True)
        linker.add_lib_flags("yaxt", ["-lyaxt", "-lyaxt_c"])
        linker.add_lib_flags("xios", ["-lxios"])
        linker.add_lib_flags("hdf5", ["-lhdf5"])

        # Always link with C++ libs
        linker.add_post_lib_flags(["-lstdc++"])
