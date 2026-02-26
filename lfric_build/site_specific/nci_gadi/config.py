#! /usr/bin/env python3

'''
This module contains the default configuration for NCI. It will be invoked
by the Baf scripts. This script:
- sets intel-classic as the default compiler suite to use.
- Adds the tau compiler wrapper as (optional) compilers to the ToolRepository.
'''

from pathlib import Path
from typing import List, Union, Optional

from fab.api import (BuildConfig, Category, Compiler, CompilerWrapper,
                     Linker, ToolRepository)
from fab.tools.compiler import FortranCompiler

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
                     add_flags: Union[None, List[str]] = None,
                     syntax_only: Optional[bool] = None) -> None:
        '''
        This method overrides the Fab CompilerWrapper class compile_file
        method to fall back to the wrapped compiler for certain Fortran files
        and use the tau_f90.sh wrapper to compile the rest.

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
            assert isinstance(self.compiler, FortranCompiler)
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
        self.add_tau(self)

    def add_tau(self, build_config: BuildConfig):
        """
        Adds the tau compiler and linker wrapper for gfortran/gcc and
        ifort/icc to the tool repository.

        :param build_config: the BuildConfig instance.
        """
        tr = ToolRepository()
        # Add the tau wrappers for Fortran and C. Note that add_tool
        # will automatically add them as a linker as well.
        for ftn in ["ifort", "gfortran"]:
            compiler = tr.get_tool(Category.FORTRAN_COMPILER, ftn)
            assert isinstance(compiler, FortranCompiler)    # mypy
            tr.add_tool(Tauf90(compiler))

        for cc in ["icc", "gcc"]:
            compiler = tr.get_tool(Category.C_COMPILER, cc)
            assert isinstance(compiler, Compiler)    # mypy
            tr.add_tool(Taucc(compiler))

    def setup_intel_classic(self, build_config: BuildConfig):
        """
        Sets up the Intel classic compiler suite. ATM adds the flags for
        compiling and linking with NetCDF.

        :param build_config: the BuildConfig instance.
        """
        super().setup_intel_classic(build_config)
        tr = ToolRepository()
        ifort = tr.get_tool(Category.FORTRAN_COMPILER, "ifort")
        assert isinstance(ifort, FortranCompiler)
        self.setup_compiler(ifort)
        linker_ifort = tr.get_tool(Category.LINKER, "linker-ifort")
        assert isinstance(linker_ifort, Linker)
        self.setup_linker(linker_ifort)

        # Always link with C++ libs
        linker_ifort.add_post_lib_flags(["-lstdc++"])

    def setup_intel_llvm(self, build_config: BuildConfig):
        """
        Sets up the Intel LLVM compiler suite. ATM adds the flags for
        compiling and linking with NetCDF.

        :param build_config: the BuildConfig instance.
        """
        super().setup_intel_llvm(build_config)
        tr = ToolRepository()
        ifx = tr.get_tool(Category.FORTRAN_COMPILER, "ifx")
        assert isinstance(ifx, FortranCompiler)
        self.setup_compiler(ifx)
        linker_ifx = tr.get_tool(Category.LINKER, "linker-ifx")
        assert isinstance(linker_ifx, Linker)
        self.setup_linker(linker_ifx)

        # Always link with C++ libs
        linker_ifx.add_post_lib_flags(["-lstdc++"])

    def setup_gnu(self, build_config: BuildConfig):
        """
        Sets up the GNU compiler suite. ATM adds the flags for
        compiling and linking with NetCDF.

        :param build_config: the BuildConfig instance.
        """
        super().setup_gnu(build_config)
        tr = ToolRepository()
        gfortran = tr.get_tool(Category.FORTRAN_COMPILER, "gfortran")
        assert isinstance(gfortran, FortranCompiler)
        self.setup_compiler(gfortran)
        linker_gfortran = tr.get_tool(Category.LINKER, "linker-gfortran")
        assert isinstance(linker_gfortran, Linker)
        self.setup_linker(linker_gfortran)

        # Always link with C++ libs
        linker_gfortran.add_post_lib_flags(["-lstdc++"])

    def setup_compiler(self, compiler: Compiler) -> None:
        """
        Used to add 'generic' flags to the compiler. ATM adds the
        flags for using NetCDF based on nf-config output (which is
        actually compiler independent).

        :param compiler: The compiler to add the flags to.
        """
        tr = ToolRepository()
        shell = tr.get_default(Category.SHELL)
        # We must remove the trailing new line, and create a list:
        nf_flags = shell.run(additional_parameters=["-c",
                                                    "nf-config --fflags"],
                             capture_output=True).strip().split()
        compiler.add_flags(nf_flags)

    def setup_linker(self, linker: Linker):
        """
        Used to add 'generic' flags to the linker. ATM adds the
        flags for using NetCDF based on nf-config output (which is
        actually compiler independent).

        :param linker: The linker to add the flags to.
        """
        tr = ToolRepository()
        shell = tr.get_default(Category.SHELL)
        # We must remove the trailing new line, and create a list:
        nc_flibs = shell.run(additional_parameters=["-c", "nf-config --flibs"],
                             capture_output=True).strip().split()
        linker.add_lib_flags("netcdf", nc_flibs, silent_replace=True)
