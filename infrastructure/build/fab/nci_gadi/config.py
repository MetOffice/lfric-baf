#! /usr/bin/env python3

'''This module contains the default configuration for NCI. It will be invoked
by the Baf scripts. This script:
- sets intel-classic as the default compiler suite to use.
- Adds the tau compiler wrapper as (optional) compilers to the ToolRepository.

'''


from fab.tools import (Category, Compiler, CompilerWrapper, Tool,
                       ToolRepository)

from default.config import Config as DefaultConfig


class Shell(Tool):
    '''A simple wrapper that runs a shell script.
    :name: the path to the script to run.
    '''
    def __init__(self, name: str):
        super().__init__(name=name, exec_name=name,
                         category=Category.MISC)

    def check_available(self):
        return True


class Tauf90(CompilerWrapper):
    '''Class for the Tau profiling Fortran compiler wrapper.
    It will be using the name "tau-COMPILER_NAME", but will call tau_f90.sh.

    :param compiler: the compiler that the tau_f90.sh wrapper will use.
    '''

    def __init__(self, compiler: Compiler):
        super().__init__(name=f"tau-{compiler.name}",
                         exec_name="tau_f90.sh", compiler=compiler, mpi=True)

    def compile_file(self, input_file,
                     output_file,
                     openmp,
                     add_flags=None,
                     syntax_only=None):
        if ('psy.f90' in str(input_file)) or \
          ('/kernel/' in str(input_file)) or \
          ('leaf_jls_mod' in str(input_file)) or \
          ('/science/' in str(input_file)):
            self.compiler.compile_file(input_file, output_file,
                                       openmp, add_flags, syntax_only)
        else:
            super().compile_file(input_file, output_file,
                                 openmp, add_flags, syntax_only)


class Taucc(CompilerWrapper):
    '''Class for the Tau profiling C compiler wrapper.
    It will be using the name "tau-COMPILER_NAME", but will call tau_cc.sh.

    :param compiler: the compiler that the tau_cc.sh wrapper will use.
    '''

    def __init__(self, compiler: Compiler):
        super().__init__(name=f"tau-{compiler.name}",
                         exec_name="tau_cc.sh", compiler=compiler, mpi=True)


class Config(DefaultConfig):
    '''For NCI, make intel the default, and add the Tau wrapper.
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

        # ATM a linker is not using a compiler wrapper, and so
        # linker-mpif90-gfortran does not inherit from linker-gfortran.
        # For now set the flags in both linkers:
        bash = Shell("bash")
        # We must remove the trailing new line, and create a list:
        nc_flibs = bash.run(additional_parameters=["-c", "nf-config --flibs"],
                            capture_output=True).strip().split()
        linker = tr.get_tool(Category.LINKER, "linker-tau-ifort")
        linker.add_lib_flags("netcdf", nc_flibs, silent_replace=True)
        linker.add_lib_flags("yaxt", ["-lyaxt", "-lyaxt_c"])
        linker.add_lib_flags("xios", ["-lxios"])
        linker.add_lib_flags("hdf5", ["-lhdf5"])

        # Always link with C++ libs
        linker.add_post_lib_flags(["-lstdc++"])
