#! /usr/bin/env python3

from fab.tools import ToolRepository

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
