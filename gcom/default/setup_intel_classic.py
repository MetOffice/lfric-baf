#!/usr/bin/env python3

'''This file contains a function that sets the default flags for all
Intel classic based compilers in the ToolRepository (ifort, icc).

This function gets called from the default site-specific config file
'''

import argparse
from typing import cast

from fab.build_config import BuildConfig
from fab.tools import Category, Compiler, Linker, ToolRepository


def setup_intel_classic(build_config: BuildConfig, args: argparse.Namespace):
    # pylint: disable=unused-argument, too-many-locals
    '''Defines the default flags for all Intel classic compilers.

    :para build_config: the build config from which required parameters
        can be taken.
    :param args: all command line options
    '''

    tr = ToolRepository()
    ifort = tr.get_tool(Category.FORTRAN_COMPILER, "ifort")
    ifort = cast(Compiler, ifort)

    if not ifort.is_available:
        # Since some flags depends on version, the code below requires
        # that the intel compiler actually works.
        return

    # The base flags
    # ==============
    # The following flags will be applied to all modes:
    ifort.add_flags(["-stand", "f08"],               "base")
    ifort.add_flags(["-g", "-traceback"],            "base")
    # With -warn errors we get externals that are too long. While this
    # is a (usually safe) warning, the long externals then causes the
    # build to abort. So for now we cannot use `-warn errors`
    ifort.add_flags(["-warn", "all"],                "base")

    # By default turning interface warnings on causes "genmod" files to be
    # created. This adds unnecessary files to the build so we disable that
    # behaviour.
    ifort.add_flags(["-gen-interfaces", "nosource"], "base")

    # The "-assume realloc-lhs" switch causes Intel Fortran prior to v17 to
    # actually implement the Fortran2003 standard. At version 17 it becomes the
    # default behaviour.
    if ifort.get_version() < (17, 0):
        ifort.add_flags(["-assume", "realloc-lhs"], "base")

    # Full debug
    # ==========
    # ifort.mk: bad interaction between array shape checking and
    # the matmul" intrinsic in at least some iterations of v19.
    if (19, 0, 0) <= ifort.get_version() < (19, 1, 0):
        runtime_flags = ["-check", "all,noshape", "-fpe0"]
    else:
        runtime_flags = ["-check", "all", "-fpe0"]
    ifort.add_flags(runtime_flags,        "full-debug")
    ifort.add_flags(["-O0", "-ftrapuv"],  "full-debug")

    # Fast debug
    # ==========
    ifort.add_flags(["-O2", "-fp-model=strict"], "fast-debug")

    # Production
    # ==========
    ifort.add_flags(["-O3", "-xhost"], "production")
