#!/usr/bin/env python3
# ##############################################################################
#  (c) Crown copyright Met Office. All rights reserved.
#  For further details please refer to the file COPYRIGHT
#  which you should have received as part of this distribution
# ##############################################################################

'''
This module contains an ExtractMixin class to add support for all extration
scripts.
'''

import logging
from pathlib import Path

from fab.api import BuildConfig, Category
from fab.artefacts import ArtefactSet
from fab.steps import run_mp, step
from fab.util import TimerLogger

from transmute_info import TransmuteInfo

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TransmuteStep:
    '''
    This is a mixin class for transmutation (i.e. transforming existing
    Fortran files with PSyclone). It is implemented as a mixin to

    '''

    def __init__(self,
                 config: BuildConfig,
                 site: str,
                 platform: str):
        self._config = config
        self._site = site
        self._platform = platform

    @step
    def transmute_step(self, transmute_file_list: list[str]) -> None:
        """
        This is the transmute step (which is called from LFRicBase before
        running PSyclone in DSL mode). It takes a list of transmutation file
        names, which are file(s) which specify which scripts should be
        applied.
        """
        if not transmute_file_list:
            return

        # This ensures that PSyclone exists and is marked as available
        _ = self._config.tool_box.get_tool(Category.PSYCLONE)

        ti = TransmuteInfo()

        for transmute_file in transmute_file_list:
            ti.import_makefile(transmute_file)

        args = []
        opt_dir = (self._config.source_root / "optimisation" /
                   f"{self._site}-{self._platform}" / "transmute")

        for filename in ti.get_transmute_files():
            args.append((self._config, opt_dir, filename))

        with TimerLogger(f"running transmute on {len(args)} "
                         f"files"):
            results = run_mp(self._config, args, self.transmute_one_file)

        # Analyse the results, log any message as required, and remove
        # the original names from the artefact store, and add the new ones.
        remove_files: list[str] = []
        add_files: list[str] = []
        for message, old_new_names in results:
            if message:
                logger.info(message)
            for old_name, new_name in old_new_names:
                remove_files.append(old_name)
                add_files.append(new_name)
        self._config.artefact_store.replace(ArtefactSet.FORTRAN_COMPILER_FILES,
                                            remove_files, add_files)

    @staticmethod
    def transmute_one_file(
            args: tuple[BuildConfig, str, str]) -> tuple[
                str, list[tuple[Path, Path]]]:
        """
        This function is responsible for applying a given script to a file.
        It receives three parameters (in one tuple, since it's called in
        parallel):
        config: the BuildConfig
        opt_dir: the (site- and platform-specific) transmute directory
        script: the 'core' name of the script (without .py)

        It applies the script to the file with the same core name and `.f90`
        suffix.

        :param args: a tuple consisting of the config, opt_dir, and the script
            name.

        :returns: a tuple consisting of messages for the user (since logging
            messages will likely get lost) and a list of pairs with the old
            name and the new name of the transformed file.
        """

        config, opt_dir, script_name = args

        # First find the files to which to apply the transmutation

        # Only the 'name' (without path) is given as script file. The
        # expected source file name must have `.f90` suffix:
        accepted_file = f"{script_name}.f90"
        f90_files = config.artefact_store[ArtefactSet.FORTRAN_COMPILER_FILES]
        transmute_files = [i for i in f90_files if i.name == accepted_file]

        if not transmute_files:
            msg = f"No file found for transmuting '{script_name}'."
            logger.info(msg)
            # That might be ok, so ignore this. Return the message
            # and an empty list of new/old names.
            return msg, []

        # Then find if there actually is an optimisation file with the same
        # relative part as each source file found:
        psyclone = config.tool_box.get_tool(Category.PSYCLONE)
        # Collect pairs of old-name, transformed-name)
        result: list[tuple(str, str)] = []
        # Collect warning messages
        messages = ""

        # ATM there is only one possible file (since file names must be unique
        # in Fab, but in the future we might want to support one script to be
        # applied to several files):
        for transmute_file in transmute_files:
            relative_path = transmute_file.relative_to(config.build_output)

            local_transformation_script = (
                opt_dir / relative_path.with_suffix('.py'))
            if not local_transformation_script.exists():
                msg = (f"Cannot find transformation script for "
                       f"file '{transmute_file}' -> "
                       f"'{local_transformation_script}' in"
                       f"'{opt_dir}'.")
                logger.info(msg)
                messages = f"{messages}\n{msg}"
                continue

            out_file = transmute_file.with_suffix(".processed.f90")
            # The PSyclone tool expects a function which returns the
            # name of the script to use (based on the filename and
            # configuration). Therefore, provide a lambda that returns
            # the required name:

            def get_trans_script(_1, _2, script=local_transformation_script):
                """
                This function returns the transformation script to use
                (depending on file name=_1 and config=_2). Here we need to
                return the fixed name. We provide it as default parameter
                due to pylint warning about `cell-var-from-loop`
                """
                return script

            psyclone.process(config=config,
                             api=None,
                             x90_file=transmute_file,
                             transformed_file=out_file,
                             transformation_script=get_trans_script)
            result.append((transmute_file, out_file))

        # Return any messages and the old/new names info
        return messages, result
