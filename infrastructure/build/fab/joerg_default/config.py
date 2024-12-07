#! /usr/bin/env python3

from fab.tools import Category, ToolRepository

from default.config import Config as DefaultConfig


class Config(DefaultConfig):
    '''We need additional include flags for gfortran. Define this
    by overwriting setup_gnu.
    Also make gnu the default compiler.
    '''

    def __init__(self):
        super().__init__()
        tr = ToolRepository()
        tr.set_default_compiler_suite("gnu")

    def setup_gnu(self, build_config):
        '''Define default compiler flags for GNU.
        '''

        super().setup_gnu(build_config)
        gfortran = ToolRepository().get_tool(Category.FORTRAN_COMPILER,
                                             "gfortran")
        gfortran.add_flags(
            [
                # The lib directory contains mpi.mod
                '-I', ('/home/joerg/work/spack/var/spack/environments/'
                       'lfric-v0/.spack-env/view/lib'),
                # mod_wait.mod
                '-I', ('/home/joerg/work/spack/var/spack/environments/'
                       'lfric-v0/.spack-env/view/include'),
                '-DITSUPERWORKS'
            ])
        for linker_name in ["linker-gfortran", "linker-mpif90-gfortran"]:
            gfortran = ToolRepository().get_tool(Category.LINKER, linker_name)
            gfortran.add_post_lib_flags(
                ['-L', ('/home/joerg/work/spack/var/spack/'
                        'environments/lfric-v0/.spack-env/view/lib')])
