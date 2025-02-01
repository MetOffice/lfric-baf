#!/usr/bin/env python3
# ##############################################################################
#  (c) Crown copyright Met Office. All rights reserved.
#  For further details please refer to the file COPYRIGHT
#  which you should have received as part of this distribution
# ##############################################################################

'''This is a mixin that will add support for extraction. It is important to be
added first as base class so that the methods overwritten here will be called.
If the derived class also needs to overwrite e.f. the psyclone method, it
must take care to call the right base class implementation(s).
'''

import logging
import shutil

from fab.artefacts import ArtefactSet
from fab.steps import run_mp, step
from fab.steps.grab.folder import grab_folder
from fab.util import file_checksum, log_or_dot, TimerLogger

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ExtractMixin:

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
                       'Removing private using fparser remove_private')
            from make_public import remove_private
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

    def grab_files(self):
        super().grab_files()
        grab_folder(self.config, src=self.lfric_core_root /
                    "infrastructure" / "build" / "psyclone" / "psydata"
                    / "extract", dst_label='psydata')

    def psyclone(self):
        self.remove_private()
        super().psyclone()

    def get_transformation_script(self, fpath, config):
        ''':returns: the transformation script to be used by PSyclone.
        :rtype: Path
        '''
        return config.source_root / 'optimisation' / 'extract' / 'global.py'
