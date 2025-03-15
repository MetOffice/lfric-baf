#! /usr/bin/env python3


'''This module contains the default Baf configuration class.
'''

import argparse
from typing import List

from fab.build_config import BuildConfig
from fab.tools import Category, ToolRepository

from default.setup_cray import setup_cray
from default.setup_gnu import setup_gnu
from default.setup_intel_classic import setup_intel_classic
from default.setup_intel_llvm import setup_intel_llvm
from default.setup_nvidia import setup_nvidia


class Config:
    '''This class is the default Configuration object for Baf builds.
    It provides several callbacks which will be called from the build
    scripts to allow site-specific customisations.
    '''

    def __init__(self):
        self._args = None

    @property
    def args(self):
        ''':returns: the command line options specified by the user.
        '''
        return self._args

    def get_valid_profiles(self) -> List[str]:
        '''Determines the list of all allowed compiler profiles. The first
        entry in this list is the default profile to be used. This method
        can be overwritten by site configs to add or modify the supported
        profiles.

        :returns: list of all supported compiler profiles.
        '''
        return ["full-debug", "fast-debug", "production", "unit-tests"]

    def update_toolbox(self, build_config: BuildConfig):
        '''Set the default compiler flags for the various compiler
        that are supported.
        '''
        # First create the default compiler profiles for all available
        # compilers:
        tr = ToolRepository()
        for compiler in (tr[Category.C_COMPILER] +
                         tr[Category.FORTRAN_COMPILER]):
            if compiler.is_available:
                # Define a base profile, which contains the common
                # compilation flags. This 'base' is not accessible to
                # the user, so it's not part of the profile list
                compiler.define_profile("base")
                for profile in self.get_valid_profiles():
                    compiler.define_profile(profile, "base")

        self.setup_intel_classic(build_config)
        self.setup_intel_llvm(build_config)
        self.setup_gnu(build_config)
        self.setup_nvidia(build_config)
        self.setup_cray(build_config)

    def handle_command_line_options(self, args: argparse.Namespace):
        '''Additional callback function executed once all command line
        options have been added. This is for example used to add
        Vernier profiling flags, which are site-specific.
        '''
        # Keep a copy of the args, so they can be used when
        # initialising compilers
        self._args = args

    def setup_cray(self, build_config: BuildConfig):
        '''For now call an external function, since it is expected that
        this configuration can be very lengthy (once we support
        compiler modes).
        '''
        setup_cray(build_config, self.args)

    def setup_gnu(self, build_config: BuildConfig):
        '''For now call an external function, since it is expected that
        this configuration can be very lengthy (once we support
        compiler modes).
        '''
        setup_gnu(build_config, self.args)

    def setup_intel_classic(self, build_config):
        '''For now call an external function, since it is expected that
        this configuration can be very lengthy (once we support
        compiler modes).
        '''
        setup_intel_classic(build_config, self.args)

    def setup_intel_llvm(self, build_config: BuildConfig):
        '''For now call an external function, since it is expected that
        this configuration can be very lengthy (once we support
        compiler modes).
        '''
        setup_intel_llvm(build_config, self.args)

    def setup_nvidia(self, build_config: BuildConfig):
        '''For now call an external function, since it is expected that
        this configuration can be very lengthy (once we support
        compiler modes).
        '''
        setup_nvidia(build_config, self.args)
