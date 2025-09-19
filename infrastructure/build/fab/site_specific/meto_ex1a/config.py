#! /usr/bin/env python3

'''This module contains a setup for METO-EX1A
'''

from typing import cast

from fab.tools import Category, Linker, ToolRepository
from fab.build_config import BuildConfig

from default.config import Config as DefaultConfig


class Config(DefaultConfig):
    '''This config class sets specific flags for METO-EX1A
    '''

    def __init__(self):
        super().__init__()
        tr = ToolRepository()
        # Set cray as default compiler suite
        # It has crayftn-ftn as Fortran compiler
        # It also has craycc-cc as C compiler
        tr.set_default_compiler_suite("cray")

    def setup_cray(self, build_config: BuildConfig):
        '''First call the base class to get all default options.
        See the file ../default/setup_cray.py for the current
        default.
        Very likely, linker options need to be changed:
        '''
        super().setup_cray(build_config)
        tr = ToolRepository()
        ftn = tr.get_tool(Category.FORTRAN_COMPILER, "crayftn-ftn")

        # Update the linker. This is what the default sets up
        # (except NetCDF, which is normally defined using nf-config
        linker = tr.get_tool(Category.LINKER, "linker-crayftn-ftn")
        linker = cast(Linker, linker)   # make mypy happy

        # Don't know whether Cray uses nf-config. So hard-code
        # these flags for now until the transition to pkg-config
        linker.add_lib_flags("netcdf", ["-lnetcdff", "-lnetcdf",
                                        "-lnetcdf", "-lm"])
        # That's pretty much the default:
        linker.add_lib_flags("yaxt", ["-lyaxt", "-lyaxt_c"])
        linker.add_lib_flags("xios", ["-lxios"])
        linker.add_lib_flags("hdf5", ["-lhdf5"])
        linker.add_lib_flags("shumlib", ["-lshum"])
        linker.add_lib_flags("vernier", ["-lvernier_f", "-lvernier_c", "-lvernier"])
