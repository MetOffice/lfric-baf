#!/usr/bin/python3

'''
This module contains the Fab Templaterator class.
'''

import logging
from pathlib import Path
from typing import Dict

from fab.tools import Tool

logger = logging.getLogger('fab')


class Templaterator(Tool):
    '''This implements the LFRic templaterator as a Fab tool.
    It can check whether the templaterator is available and
    creates command line options for it to run.

    :param Path path: the path to the templaterator binary.
    '''
    def __init__(self, exec_name: Path):
        super().__init__(exec_name.name, exec_name=str(exec_name))

    def check_available(self) -> bool:
        '''
        :returns bool: whether templaterator works by running
        `Templaterator -help`.
        '''
        try:
            super().run(additional_parameters="-h")
        except RuntimeError:
            return False

        return True

    def run(self, input_template: Path,
            output_file: Path,
            key_values: Dict) -> None:
        # pylint: disable=arguments-differ
        '''
        This wrapper creates the proper command line options for
        the Templaterator.

        :param Path input_template: the path to the input template.
        :param Path output_file: the output file path.
        :param Dict key_values: the keys and values for the keys to
        define as a dictionary.
        '''
        replace = [f"-s {key}={value}" for key, value in key_values.items()]
        params = [input_template, "-o", output_file]+replace
        super().run(additional_parameters=params)


# =============================================================================
if __name__ == "__main__":
    '''
    A small test for the Templaterator tool.
    '''
    # That's in general useless, since it only works when invoked from
    # the right directory - but better than nothing.
    templaterator = Templaterator(Path("lfric_core/infrastructure/build/"
                                       "tools/Templaterator"))
    print("Templaterator available:", templaterator.is_available)
