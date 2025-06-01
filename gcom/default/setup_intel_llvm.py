#!/usr/bin/env python3

'''This file contains a function that sets the default flags for all
Intel llvm based compilers in the ToolRepository (ifx, icx).

This function gets called from the default site-specific config file
'''

import argparse
from typing import cast

from fab.build_config import BuildConfig
from fab.tools import Category, Compiler, Linker, ToolRepository


def setup_intel_llvm(build_config: BuildConfig, args: argparse.Namespace):
    # pylint: disable=unused-argument, too-many-locals
    '''Defines the default flags for all Intel llvm compilers.

    :para build_config: the build config from which required parameters
        can be taken.
    :param args: all command line options
    '''

    tr = ToolRepository()
    ifx = tr.get_tool(Category.FORTRAN_COMPILER, "ifx")
    ifx = cast(Compiler, ifx)

    if not ifx.is_available:
        return

    # The base flags
    # ==============
    # The following flags will be applied to all modes:
    ifx.add_flags(["-stand", "f08"],               "base")
    ifx.add_flags(["-g", "-traceback"],            "base")
    # With -warn errors we get externals that are too long. While this
    # is a (usually safe) warning, the long externals then causes the
    # build to abort. So for now we cannot use `-warn errors`
    ifx.add_flags(["-warn", "all"],                "base")

    # By default turning interface warnings on causes "genmod" files to be
    # created. This adds unnecessary files to the build so we disable that
    # behaviour.
    ifx.add_flags(["-gen-interfaces", "nosource"], "base")

    # Full debug
    # ==========
    ifx.add_flags(["-check", "all", "-fpe0"], "full-debug")
    ifx.add_flags(["-O0", "-ftrapuv"],        "full-debug")

    # Fast debug
    # ==========
    ifx.add_flags(["-O2", "-fp-model=strict"], "fast-debug")

    # Production
    # ==========
    ifx.add_flags(["-O3", "-xhost"], "production")
