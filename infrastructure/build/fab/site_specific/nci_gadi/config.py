#! /usr/bin/env python3

'''
This module contains the default configuration for NCI. It will be invoked
by the Baf scripts. This script:
- sets intel-classic as the default compiler suite to use.
- Adds the tau compiler wrapper as (optional) compilers to the ToolRepository.
'''

from pathlib import Path
from typing import List, Union, Optional

from fab.build_config import BuildConfig
from fab.tools import (Category, Compiler, CompilerWrapper,
                       ToolRepository)

from default.config import Config as DefaultConfig


class Tauf90(CompilerWrapper):
    '''
    Class for the Tau profiling Fortran compiler wrapper.
    It will be using the name "tau-COMPILER_NAME", but will call tau_f90.sh.

    :param compiler: the compiler that the tau_f90.sh wrapper will use.
    :type compiler: :py:class:`fab.tools.Compiler`
    '''

    def __init__(self, compiler: Compiler):
        super().__init__(name=f"tau-{compiler.name}",
                         exec_name="tau_f90.sh", compiler=compiler, mpi=True)

    def compile_file(self, input_file: Path,
                     output_file: Path,
                     config: BuildConfig,
                     add_flags:Union[None, List[str]] = None,
                     syntax_only: Optional[bool] = None) -> None:
        '''
        This method overrides the Fab CompilerWrapper class compile_file
        method to fall back to the wrapped compiler for certain Fortran files and
        use the tau_f90.sh wrapper to compile the rest.

        :param Path input_file: the path of the input file to compile
        :param Path output_file: the path of the output file to create
        :param config: the Fab build configuration instance
        :type config: :py:class:`fab.BuildConfig`
        :param add_flags: additional flags to pass to the compiler
        :type add_flags: Union[None, List[str]]
        :param syntax_only: whether to only check the syntax of the file
        :type syntax_only: Optional[bool]
        '''
        if ('psy.f90' in str(input_file)) or \
          ('/kernel/' in str(input_file)) or \
          ('leaf_jls_mod' in str(input_file)) or \
          ('/science/' in str(input_file)):
            self.compiler.compile_file(input_file, output_file,
                                       config, add_flags, syntax_only)
        else:
            super().compile_file(input_file, output_file,
                                 config, add_flags, syntax_only)


class Taucc(CompilerWrapper):
    '''
    Class for the Tau profiling C compiler wrapper.
    It will be using the name "tau-COMPILER_NAME", but will call tau_cc.sh.

    :param compiler: the compiler that the tau_cc.sh wrapper will use
    :type compiler: :py:class:`fab.tools.Compiler`
    '''

    def __init__(self, compiler: Compiler):
        super().__init__(name=f"tau-{compiler.name}",
                         exec_name="tau_cc.sh", compiler=compiler, mpi=True)


class Config(DefaultConfig):
    '''
    For NCI, make intel the default, and add the Tau wrapper.
    '''

    def __init__(self):
        super().__init__()
        tr = ToolRepository()
        tr.set_default_compiler_suite("intel-classic")

        # Add the tau wrappers for Fortran and C. Note that add_tool
        # will automatically add them as a linker as well.
        for ftn in ["ifort", "gfortran"]:
            compiler = tr.get_tool(Category.FORTRAN_COMPILER, ftn)
            tr.add_tool(Tauf90(compiler))

        for cc in ["icc", "gcc"]:
            compiler = tr.get_tool(Category.C_COMPILER, cc)
            tr.add_tool(Taucc(compiler))

        # ATM we don't use a shell when running a tool, and as such
        # we can't directly use "$()" as parameter. So query these values using
        # Fab's shell tool (doesn't really matter which shell we get, so just
        # ask for the default):
        shell = tr.get_default(Category.SHELL)
        # We must remove the trailing new line, and create a list:
        nc_flibs = shell.run(additional_parameters=["-c", "nf-config --flibs"],
                             capture_output=True).strip().split()
        linker = tr.get_tool(Category.LINKER, "linker-tau-ifort")
        linker.add_lib_flags("netcdf", nc_flibs)
        linker.add_lib_flags("yaxt", ["-lyaxt", "-lyaxt_c"])
        linker.add_lib_flags("xios", ["-lxios"])
        linker.add_lib_flags("hdf5", ["-lhdf5"])

        # Always link with C++ libs
        linker.add_post_lib_flags(["-lstdc++"])
