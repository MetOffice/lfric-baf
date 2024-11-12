#!/usr/bin/env python3
# ##############################################################################
#  (c) Crown copyright Met Office. All rights reserved.
#  For further details please refer to the file COPYRIGHT
#  which you should have received as part of this distribution
# ##############################################################################

'''A FAB build script for gungho_model. It relies on the FabBase class
contained in the infrastructure directory.
'''

import logging
import shutil

from fab.artefacts import ArtefactSet
from fab.steps import run_mp, step
from fab.util import file_checksum, log_or_dot, TimerLogger

from fab_gungho_model import FabGungho


class FabGunghoExtract(FabGungho):

    @staticmethod
    def remove_one_private(args):
        state, fpath = args
        hash = file_checksum(fpath).file_hash
        no_private_fpath = (state.prebuild_folder /
                            f'no-private-{fpath.stem}.{hash}{fpath.suffix}')

        if no_private_fpath.exists():
            log_or_dot(logger,
                       f'Removing private using prebuild: \
                        {no_private_fpath}')
            shutil.copy(no_private_fpath, fpath)
        else:
            log_or_dot(logger,
                       f'Removing private using fparser remove_private')
            from remove_private import remove_private
            from psyclone.line_length import FortLineLength
            fll = FortLineLength()
            tree = remove_private(str(fpath))
            code = fll.process(str(tree))
            open(fpath, "wt").write(code)
            open(no_private_fpath, "wt").write(code)

        return no_private_fpath

    @step
    def remove_private(self):
        state = self.config
        input_files = state.artefact_store[ArtefactSet.FORTRAN_BUILD_FILES]
        args = [(state, filename) for filename in input_files]
        with TimerLogger(f"running remove-private on {len(input_files)} "
                         f"f90 files"):
            results = run_mp(state, args, self.remove_one_private)
        # Add the cached data to the prebuilds, so that the cleanup
        # at the end of the run will not delete these files.
        state.add_current_prebuilds(results)

    def psyclone(self):
        self.remove_private()
        super().psyclone()

    def get_transformation_script(self, fpath, config):
        ''':returns: the transformation script to be used by PSyclone.
        :rtype: Path
        '''
        return config.source_root / 'optimisation' / 'extract' / 'global.py'


# -----------------------------------------------------------------------------
if __name__ == '__main__':

    logger = logging.getLogger('fab')
    logger.setLevel(logging.DEBUG)
    fab_gungo = FabGunghoExtract(name="gungho_model_extract",
                                 root_symbol="gungho_model")
    fab_gungo.build()
