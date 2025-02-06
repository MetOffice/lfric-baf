#! /usr/bin/env python3


'''This module contains the default Baf configuration class.
'''

import argparse

from fab.build_config import BuildConfig

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

    def update_toolbox(self, build_config: BuildConfig):
        '''Set the default compiler flags for the various compiler
        that are supported.
        '''
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
        setup_cray(build_config, self._args)

    def setup_gnu(self, build_config: BuildConfig):
        '''For now call an external function, since it is expected that
        this configuration can be very lengthy (once we support
        compiler modes).
        '''
        setup_gnu(build_config, self._args)

    def setup_intel_classic(self, build_config):
        '''For now call an external function, since it is expected that
        this configuration can be very lengthy (once we support
        compiler modes).
        '''
        setup_intel_classic(build_config, self._args)

    def setup_intel_llvm(self, build_config: BuildConfig):
        '''For now call an external function, since it is expected that
        this configuration can be very lengthy (once we support
        compiler modes).
        '''
        setup_intel_llvm(build_config, self._args)

    def setup_nvidia(self, build_config: BuildConfig):
        '''For now call an external function, since it is expected that
        this configuration can be very lengthy (once we support
        compiler modes).
        '''
        setup_nvidia(build_config, self._args)
