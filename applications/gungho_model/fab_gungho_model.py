#!/usr/bin/env python3
# ##############################################################################
#  (c) Crown copyright Met Office. All rights reserved.
#  For further details please refer to the file COPYRIGHT
#  which you should have received as part of this distribution
# ##############################################################################

'''A FAB build script for gungho_model. It relies on the LFRicBase class
contained in the infrastructure directory.
'''

import logging

from fab.steps.grab.folder import grab_folder

from lfric_base import LFRicBase


class FabGungho(LFRicBase):

    def grab_files(self):
        super().grab_files()
        dirs = ['applications/gungho_model/source/',
                'science/gungho/source',
                'science/shared/source/',
                ]
        # pylint: disable=redefined-builtin
        for dir in dirs:
            grab_folder(self.config, src=self.lfric_apps_root / dir,
                        dst_label='')

        # Copy the optimisation scripts into a separate directory
        dir = 'applications/gungho_model/optimisation'
        grab_folder(self.config, src=self.lfric_apps_root / dir,
                    dst_label='optimisation')

    def get_rose_meta(self):
        return (self.lfric_apps_root / 'applications' / 'gungho_model'
                / 'rose-meta' / 'lfric-gungho_model' / 'HEAD'
                / 'rose-meta.conf')


# -----------------------------------------------------------------------------
if __name__ == '__main__':

    logger = logging.getLogger('fab')
    logger.setLevel(logging.DEBUG)
    fab_gungo = FabGungho(name="gungho_model")
    fab_gungo.build()
