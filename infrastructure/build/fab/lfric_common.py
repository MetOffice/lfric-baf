import logging
import shutil
from pathlib import Path

from fab.artefacts import ArtefactSet
from fab.steps import step
from fab.steps.find_source_files import find_source_files
from fab.tools import Category, Tool

logger = logging.getLogger('fab')


class Script(Tool):
    '''A simple wrapper that runs a shell script.
    :name: the path to the script to run.
    '''
    def __init__(self, name: Path):
        super().__init__(name=name.name, exec_name=str(name),
                         category=Category.MISC)

    def check_available(self):
        return True


@step
def configurator(config, lfric_core_source: Path,
                 lfric_apps_source: Path,
                 rose_meta_conf: Path,
                 rose_picker: Tool,
                 config_dir=None):
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
        '-include_dirs', lfric_core_source])
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


@step
def fparser_workaround_stop_concatenation(config):
    """
    fparser can't handle string concat in a stop statement. This step is
    a workaround.

    https://github.com/stfc/fparser/issues/330

    """
    feign_path = None
    for file_path in config.artefact_store[ArtefactSet.FORTRAN_BUILD_FILES]:
        if file_path.name == 'feign_config_mod.f90':
            feign_path = file_path
            break
    else:
        raise RuntimeError("Could not find 'feign_config_mod.f90'.")

    # rename "broken" version
    broken_version = feign_path.with_suffix('.broken')
    shutil.move(feign_path, broken_version)

    # make fixed version
    bad = "_config: '// &\n        'Unable to close temporary file'"
    good = "_config: Unable to close temporary file'"

    open(feign_path, 'wt').write(
        open(broken_version, 'rt').read().replace(bad, good))
