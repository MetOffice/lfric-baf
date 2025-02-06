#!/usr/bin/env python3

'''This file contains a function that sets the default flags for the NVIDIA
compilers in the ToolRepository.

This function gets called from the default site-specific config file
'''

from typing import cast

from fab.build_config import BuildConfig
from fab.tools import Category, Linker, ToolRepository


def setup_nvidia(build_config: BuildConfig, offload: str = ""):
    '''Defines the default flags for nvfortran.

    :param build_config: the build config from which required parameters
        can be taken.
    :param offload: offload mode, must be one of "", "openacc", "openmp"
    '''

    offload = offload.lower()

    tr = ToolRepository()
    nvfortran = tr.get_tool(Category.FORTRAN_COMPILER, "nvfortran")
    flags = ['-Mextend',           # 132 characters line length
             '-g', '-traceback',
             '-r8',                # Default 8 bytes reals
             ]
    lib_flags = ["-c++libs"]
    nvfortran.add_flags(flags)
    if offload == "openacc":
        flags.extend(["-acc=gpu", "-gpu=managed", "-mp=multicore"])
        lib_flags.append("-cuda")
    elif offload == "openmp":
        flags.extend(["-mp=gpu", "-gpu=managed"])
        lib_flags.append("-cuda")

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
    linker = tr.get_tool(Category.LINKER, "linker-nvfortran")
    linker = cast(Linker, linker)
    linker.add_lib_flags("netcdf", nc_flibs)
    linker.add_lib_flags("yaxt", ["-lyaxt", "-lyaxt_c"])
    linker.add_lib_flags("xios", ["-lxios"])
    linker.add_lib_flags("hdf5", ["-lhdf5"])

    # Always link with C++ libs
    linker.add_post_lib_flags(lib_flags)
