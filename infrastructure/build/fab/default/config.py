#! /usr/bin/env python3


'''This module contains the default Baf configuration class.
'''

from default.setup_gnu import setup_gnu
from default.setup_intel_classic import setup_intel_classic


class Config:
    '''This class is the default Configuration object for Baf builds.
    It provides several callbacks which will be called from the build
    scripts to allow site-specific customisations.
    '''

    def update_toolbox(self, build_config):
        '''Set the default compiler flags for the various compiler
        that are supported.
        '''

        self.setup_classic_intel(build_config)
        self.setup_gnu(build_config)

    def handle_command_line_options(self, args):
        '''Additional callback function executed once all command line
        options have been added. This is for example used to add
        Vernier profiling flags, which are site-specific.
        '''

    def setup_classic_intel(self, build_config):
        '''For now call an external function, since it is expected that
        this configuration can be very lengthy (once we support
        compiler modes).
        '''
        setup_intel_classic(build_config)

    def setup_gnu(self, build_config):
        '''For now call an external function, since it is expected that
        this configuration can be very lengthy (once we support
        compiler modes).
        '''
        setup_gnu(build_config)
