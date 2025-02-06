#!/usr/bin/env python3

'''This file contains a function that sets the default flags for the Cray
compilers in the ToolRepository.

This function gets called from the default site-specific config file
'''

import argparse
from typing import cast

from fab.build_config import BuildConfig
from fab.tools import Category, Linker, ToolRepository


def setup_cray(build_config: BuildConfig, args: argparse.Namespace):
    # pylint: disable=unused-argument
    '''Defines the default flags for ftn.

    :param build_config: the build config from which required parameters
        can be taken.
    :param args: all command line options
    '''

    tr = ToolRepository()
    ftn = tr.get_tool(Category.FORTRAN_COMPILER, "crayftn-ftn")
    flags = ["-g", "-G0", "-m", "0",
             "-M", "E664,E7208,E7212",
             "-R", "bcdps",            # bounds, array shape, collapse,
                                       # pointer, string checking
             "-en",                    # Fortran standard
             "-ef",                    # use lowercase module names! Important!
             "-hnocaf",                # Required for linking with C++
             ]

    lib_flags = ["-lcraystdc++"]

    # Handle accelerator options:
    if args.openacc or args.openmp:
        host = args.host.lower()
    else:
        # Neither openacc nor openmp specified
        host = ""

    if args.openacc:
        if host == "gpu":
            flags.extend(["-h acc"])
        else:
            # CPU
            flags.extend(["-h acc"])
    elif args.openmp:
        if host == "gpu":
            flags.extend([])
        else:
            # OpenMP on CPU, that's already handled by Fab
            pass

    ftn.add_flags(flags)
    # ATM we don't use a shell when running a tool, and as such
    # we can't directly use "$()" as parameter. So query these values using
    # Fab's shell tool (doesn't really matter which shell we get, so just
    # ask for the default):
    shell = tr.get_default(Category.SHELL)
    # We must remove the trailing new line, and create a list:
    nc_flibs = shell.run(additional_parameters=["-c", "nf-config --flibs"],
                         capture_output=True).strip().split()

    # This will implicitly affect all gfortran based linkers, e.g.
    # linker-mpif90-gfortran will use these flags as well.
    linker = tr.get_tool(Category.LINKER, "linker-crayftn-ftn")
    linker = cast(Linker, linker)
    linker.add_lib_flags("netcdf", nc_flibs)
    linker.add_lib_flags("yaxt", ["-lyaxt", "-lyaxt_c"])
    linker.add_lib_flags("xios", ["-lxios"])
    linker.add_lib_flags("hdf5", ["-lhdf5"])

    linker.add_post_lib_flags(lib_flags)

    # Using the GNU compiler on Crays for now needs the additional
    # flag -fallow-argument-mismatch to compile mpi_mod.f90
    ftn = tr.get_tool(Category.FORTRAN_COMPILER, "crayftn-gfortran")
    ftn.add_flags("-fallow-argument-mismatch")
