#!/usr/bin/env python3

'''This file contains a function that sets the default flags for all
Intel classic based compilers in the ToolRepository (ifort, icc).

This function gets called from the default site-specific config file
'''

from fab.build_config import BuildConfig
from fab.tools import Category, Tool, ToolRepository


class Shell(Tool):
    '''A simple wrapper that runs a shell script.
    :name: the path to the script to run.
    '''
    def __init__(self, name: str):
        super().__init__(name=name, exec_name=name,
                         category=Category.MISC)

    def check_available(self):
        return True


def setup_intel_classic(build_config: BuildConfig):
    '''Defines the default flags for all Intel classic compilers.

    :para build_config: the build config from which required parameters
        can be taken.
    '''

    tr = ToolRepository()
    ifort = tr.get_tool(Category.FORTRAN_COMPILER, "ifort")

    if not ifort.is_available:
        # Since some flags depends on version, the code below requires
        # that the intel compiler actually works.
        return

    # The flag groups are mainly from infrastructure/build/fortran
    # /ifort.mk
    no_optimisation_flags = ['-O0']
    safe_optimisation_flags = ['-O2', '-fp-model=strict']
    risky_optimisation_flags = ['-O3', '-xhost']
    # With -warn errors we get externals that are too long. While this
    # is a (usually safe) warning, the long externals then causes the
    # build to abort. So for now we cannot use `-warn errors`
    warnings_flags = ['-warn', 'all', '-gen-interfaces', 'nosource']
    unit_warnings_flags = ['-warn', 'all', '-gen-interfaces', 'nosource']
    init_flags = ['-ftrapuv']

    # ifort.mk: bad interaction between array shape checking and
    # the matmul" intrinsic in at least some iterations of v19.
    if (19, 0, 0) <= ifort.get_version() < (19, 1, 0):
        runtime_flags = ['-check', 'all,noshape', '-fpe0']
    else:
        runtime_flags = ['-check', 'all', '-fpe0']

    # ifort.mk: option for checking code meets Fortran standard
    # - currently 2008
    fortran_standard_flags = ['-stand', 'f08']

    # ifort.mk has some app and file-specific options for older
    # intel compilers. They have not been included here
    compiler_flag_group = []

    # TODO: we need to move the compile mode into the BuildConfig
    mode = "full_debug"
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

    ifort.add_flags(compiler_flag_group)

    # ATM a linker is not using a compiler wrapper, and so
    # linker-mpif90-gfortran does not inherit from linker-gfortran.
    # For now set the flags in both linkers:
    bash = Shell("bash")
    # We must remove the trailing new line, and create a list:
    nc_flibs = bash.run(additional_parameters=["-c", "nf-config --flibs"],
                        capture_output=True).strip().split()

    for linker_name in ["linker-ifort", "linker-mpif90-ifort"]:
        linker = tr.get_tool(Category.LINKER, linker_name)
        linker.add_lib_flags("netcdf", nc_flibs, silent_replace=True)
        linker.add_lib_flags("yaxt", ["-lyaxt", "-lyaxt_c"])
        linker.add_lib_flags("xios", ["-lxios"])
        linker.add_lib_flags("hdf5", ["-lhdf5"])

        # Always link with C++ libs
        linker.add_post_lib_flags(["-lstdc++"])
