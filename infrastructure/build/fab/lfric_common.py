import logging
import shutil
from pathlib import Path
from typing import Optional

from fab.build_config import BuildConfig
from fab.artefacts import ArtefactSet
from fab.steps import step
from fab.steps.find_source_files import find_source_files
from fab.tools import Category, Tool

logger = logging.getLogger('fab')


class Script(Tool):
    '''
    A simple wrapper that runs a shell script.

    :param name: the path to the script to run.
    :type name: Path
    '''
    def __init__(self, name: Path):
        super().__init__(name=name.name, exec_name=str(name),
                         category=Category.MISC)

    def check_available(self) -> bool:
        '''
        This method overrides the base class check_available to simply
        mark the script tool as available. 
        '''
        return True


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

    # build_config_loaders
    # --------------------
    # builds a bunch of f90s from the json
    logger.info('GenerateNamelist')
    gen_namelist = Script(tools / 'GenerateNamelist')
    gen_namelist.run(additional_parameters=['-verbose', rose_meta,
                                            '-directory', config_dir],
                     cwd=config_dir)

    # create configuration_mod.f90 in source root
    # -------------------------------------------
    logger.info('GenerateLoader')
    names = [name.strip() for name in
             open(config_dir / 'config_namelists.txt').readlines()]
    configuration_mod_fpath = config_dir / 'configuration_mod.f90'
    gen_loader = Script(tools / 'GenerateLoader')
    gen_loader.run(additional_parameters=[configuration_mod_fpath,
                                          *names])

    # create feign_config_mod.f90 in source root
    # ------------------------------------------
    logger.info('GenerateFeigns')
    feign_config_mod_fpath = config_dir / 'feign_config_mod.f90'
    gft = Tool("GenerateFeignsTool", exec_name=str(tools / 'GenerateFeigns'),
               category=Category.MISC)
    gft.run(additional_parameters=[rose_meta,
                                   '-output', feign_config_mod_fpath])

    find_source_files(config, source_root=config_dir)
