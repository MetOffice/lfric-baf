##############################################################################
# (c) Crown copyright Met Office. All rights reserved.
# For further details please refer to the file COPYRIGHT
# which you should have received as part of this distribution
##############################################################################

"""
This file contains the configurator script sequence for LFRic.
"""

import logging
from pathlib import Path
from typing import cast, Optional

from fab.build_config import BuildConfig
from fab.steps import step
from fab.steps.find_source_files import find_source_files
from fab.tools import Category, Tool
from fab.tools.shell import Shell

logger = logging.getLogger('fab')


@step
def configurator(config: BuildConfig,
                 lfric_core_source: Path,
                 lfric_apps_source: Path,
                 rose_meta_conf: Path,
                 rose_picker: Tool,
                 config_dir: Optional[Path] = None) -> None:
    '''
    This method implements the LFRic configurator tool.

    :param config: the Fab build config instance
    :type config: :py:class:`fab.BuildConfig`
    :param lfric_core_source: the path to the LFRic core directory
    :type lfric_core_source: Path
    :param lfric_apps_source: the path to the LFRic apps directory
    :type lfric_apps_source: Path
    :param rose_meta_conf: the path to the rose-meta configuration file
    :type rose_meta_conf: Path
    :param rose_picker: the rose picker tool
    :type rose_picker: Tool
    :param config_dir: the directory for the generated configuration files
    :type config_dir: Optional[Path]
    '''
    # pylint: disable=too-many-arguments
    tools = lfric_core_source / 'infrastructure' / 'build' / 'tools'
    config_dir = config_dir or config.build_output / 'configuration'
    config_dir.mkdir(parents=True, exist_ok=True)

    # rose picker
    # -----------
    # creates rose-meta.json and config_namelists.txt in
    # gungho/build
    logger.info('rose_picker')

    rose_picker.run(additional_parameters=[
        rose_meta_conf,
        '-directory', config_dir,
        '-include_dirs', lfric_apps_source,
        '-include_dirs', lfric_core_source,
        '-include_dirs', lfric_core_source / 'rose-meta',
        '-include_dirs', lfric_apps_source / 'rose-meta'])
    rose_meta = config_dir / 'rose-meta.json'

    tb = config.tool_box
    shell = tb.get_tool(Category.SHELL)
    shell = cast(Shell, shell)

    # build_config_loaders
    # --------------------
    # builds a bunch of f90s from the json
    logger.info('GenerateNamelist')
    shell.exec(command=(f"{tools / 'GenerateNamelist'} -verbose {rose_meta} "
                        f"-directory {config_dir}"))

    # create configuration_mod.f90 in source root
    # -------------------------------------------
    logger.info('GenerateLoader')
    with open(config_dir / 'config_namelists.txt', encoding="utf8") as f_in:
        names = [name.strip() for name in f_in.readlines()]

    configuration_mod_fpath = config_dir / 'configuration_mod.f90'
    shell.exec(f"{tools / 'GenerateLoader'} {configuration_mod_fpath} "
               f"{' '.join(names)}")

    # create feign_config_mod.f90 in source root
    # ------------------------------------------
    logger.info('GenerateFeigns')
    feign_config_mod_fpath = config_dir / 'feign_config_mod.f90'
    shell.exec(f"{tools / 'GenerateFeigns'} {rose_meta} "
               f"-output {feign_config_mod_fpath}")

    find_source_files(config, source_root=config_dir)
