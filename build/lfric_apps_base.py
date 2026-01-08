#!/usr/bin/env python3

"""
This module contains the LFRicAppsBase class, i.e. the base class
for all LFRic applications in the lfric_apps repository.
"""
import argparse
import logging
import os
from pathlib import Path
import sys
from typing import Optional, Union

logger = logging.getLogger(__name__)

# We need to be able to import LFRicBase from the core
# repository. Scan the command line arguments for --core
# (defaulting to the $LFRIC_CORE environment variable)
# and add this to the Python search path:
arg_parser = argparse.ArgumentParser(add_help=False)
arg_parser.add_argument("--core", "-c", type=str,
                        help="Root of the LFRic core repository",
                        default="$LFRIC_CORE")
args = arg_parser.parse_known_args()[0]   # Ignore element [1]=unknown args

if args.core == "$LFRIC_CORE":
    # Default to root - it will then fail during the import
    core_path = Path(os.environ.get("LFRIC_CORE", "/"))
else:
    core_path = Path(args.core)

sys.path.insert(0, str(core_path / "infrastructure" / "build" / "fab"))

try:
    from lfric_base import LFRicBase
except ModuleNotFoundError as mnfe:
    msg = (f"Cannot import `lfric_base` from '{core_path}'. Specify a valid "
           f"location of the LFRic core repository using the --core command "
           f"line option.")
    logger.error(msg)
    raise RuntimeError(msg) from mnfe


class LFRicAppsBase(LFRicBase):
    '''
    This is the base class for all LFRic FAB scripts.

    :param name: the name to be used for the workspace. Note that
        the name of the compiler will be added to it.
    :param root_symbol: the symbol (or list of symbols) of the main
        programs. Defaults to the parameter `name` if not specified.

    '''
    # pylint: disable=too-many-instance-attributes
    def __init__(self, name: str,
                 apps_root: Path,
                 root_symbol: Optional[Union[list[str], str]] = None
                 ):
        super().__init__(name=name, apps_root=apps_root,
                         root_symbol=root_symbol)

    def define_command_line_options(
            self,
            parser: Optional[argparse.ArgumentParser] = None
            ) -> argparse.ArgumentParser:
        '''
        This adds LFRic Apps specific command line options. ATM this
        adds the flag --core (which is handled when importing this file,
        but it needs to be defined, otherwise argparse would throw
        an error).

        :param parser: optional a pre-defined argument parser.

        :returns: the argument parser with the LFRic specific options added.
        '''

        parser = super().define_command_line_options(parser)

        parser.add_argument("--core", "-c", type=str,
                            help="Root of the LFRic core repository",
                            default="$LFRIC_CORE")
        return parser
