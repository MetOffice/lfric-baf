#! /usr/bin/env python3

from default.setup_gnu import setup_gnu
from default.setup_intel_classic import setup_intel_classic


class Config:

    def update_toolbox(self, build_config):
        '''Set the default compiler flags for the various compiler
        that are supported.
        '''

        self.setup_classic_intel(build_config)
        self.setup_gnu(build_config)

    def setup_classic_intel(self, build_config):
        setup_intel_classic(build_config)

    def setup_gnu(self, build_config):
        setup_gnu(build_config)
