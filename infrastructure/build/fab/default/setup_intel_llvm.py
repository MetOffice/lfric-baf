#!/usr/bin/env python3

'''This file contains a function that sets the default flags for all
Intel llvm based compilers in the ToolRepository (ifx, icx).

This function gets called from the default site-specific config file
'''

import argparse
from typing import cast

from fab.build_config import BuildConfig
from fab.tools import Category, Linker, ToolRepository


def setup_intel_llvm(build_config: BuildConfig, args: argparse.Namespace):
    # pylint: disable=unused-argument, too-many-locals
    '''Defines the default flags for all Intel llvm compilers.

    :para build_config: the build config from which required parameters
        can be taken.
    :param args: all command line options
    '''

    tr = ToolRepository()
    ifx = tr.get_tool(Category.FORTRAN_COMPILER, "ifx")

    # The flag groups are mainly from infrastructure/build/fortran
    # /ifort.mk
    no_optimisation_flags = ['-O0']
    safe_optimisation_flags = ['-O2', '-fp-model=strict']
    risky_optimisation_flags = ['-O3', '-xhost']
    # With -warn errors we get externals that are too long. While this
    # is a (usually safe) warning, the long externals then causes the
    # build to abort. So for now we cannot use `-warn errors`
    warnings_flags = ['-warn', 'all', '-gen-interfaces', 'nosource']
    init_flags = ['-ftrapuv']

    fortran_standard_flags = ['-stand', 'f08']

    # ifort.mk has some app and file-specific options for older
    # intel compilers. They have not been included here
    compiler_flag_group = []
    runtime_flags = ['-check', 'all', '-fpe0']

    # TODO: we need to move the compilation profile into the BuildConfig
    mode = "full-debug"
    if mode == 'full-debug':
        compiler_flag_group += (warnings_flags +
                                init_flags + runtime_flags +
                                no_optimisation_flags +
                                fortran_standard_flags)
    elif mode == 'production':
        compiler_flag_group += (warnings_flags +
                                risky_optimisation_flags)
    else:  # 'fast-debug'
        compiler_flag_group += (warnings_flags +
                                safe_optimisation_flags +
                                fortran_standard_flags)

    ifx.add_flags(compiler_flag_group)

    # ATM we don't use a shell when running a tool, and as such
    # we can't directly use "$()" as parameter. So query these values using
    # Fab's shell tool (doesn't really matter which shell we get, so just
    # ask for the default):
    shell = tr.get_default(Category.SHELL)
    # We must remove the trailing new line, and create a list:
    nc_flibs = shell.run(additional_parameters=["-c", "nf-config --flibs"],
                         capture_output=True).strip().split()

    linker = tr.get_tool(Category.LINKER, "linker-ifx")
    linker = cast(Linker, linker)    # Make mypy happy
    linker.add_lib_flags("netcdf", nc_flibs, silent_replace=True)
    linker.add_lib_flags("yaxt", ["-lyaxt", "-lyaxt_c"])
    linker.add_lib_flags("xios", ["-lxios"])
    linker.add_lib_flags("hdf5", ["-lhdf5"])

    # Always link with C++ libs
    linker.add_post_lib_flags(["-lstdc++"])
