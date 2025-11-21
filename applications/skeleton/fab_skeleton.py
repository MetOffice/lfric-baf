#!/usr/bin/env python3
# ##############################################################################
#  (c) Crown copyright Met Office. All rights reserved.
#  For further details please refer to the file COPYRIGHT
#  which you should have received as part of this distribution
# ##############################################################################

'''A FAB build script for applications/skeleton. It relies on
the LFRicBase class contained in the infrastructure directory.
'''

import logging
from pathlib import Path

from fab.steps.grab.folder import grab_folder

from lfric_base import LFRicBase


class FabSkeleton(LFRicBase):
    """
    A Fab-based build script for skeleton. It relies on the LFRicBase class
    to implement the actual functionality, and only provides the required
    source files.

    :param name: The name of the application.
    """

    def __init__(self, name: str) -> None:
        this_file = Path(__file__).resolve()
        super().__init__(name=name,
                         apps_root=this_file.parents[2])
        # Store the root of this apps for later
        self._this_root = this_file.parent

    def grab_files_step(self) -> None:
        """
        Grabs the required source files and optimisation scripts.
        """
        super().grab_files_step()
        dirs = ['applications/skeleton/source/']

        # pylint: disable=redefined-builtin
        for dir in dirs:
            grab_folder(self.config, src=self.lfric_core_root / dir,
                        dst_label='')

        # Copy the optimisation scripts into a separate directory
        grab_folder(self.config, src=self._this_root / "optimisation",
                    dst_label='optimisation')

    def get_rose_meta(self) -> Path:
        """
        :returns: the rose-meta.conf path.
        """
        return (self._this_root / 'rose-meta' / 'lfric-skeleton' / 'HEAD' /
                'rose-meta.conf')


# -----------------------------------------------------------------------------
if __name__ == '__main__':

    logger = logging.getLogger('fab')
    logger.setLevel(logging.DEBUG)
    fab_skeleton = FabSkeleton(name="skeleton")
    fab_skeleton.build()
