#!/usr/bin/env python3
# ##############################################################################
#  (c) Crown copyright Met Office. All rights reserved.
#  For further details please refer to the file COPYRIGHT
#  which you should have received as part of this distribution
# ##############################################################################

'''A FAB build script for mesh_tools. It relies on the LFRicBase class
contained in the infrastructure directory.
'''

import logging

from fab.steps.grab.folder import grab_folder

from lfric_base import LFRicBase


class FabMeshTool(LFRicBase):

    def grab_files(self):
        super().grab_files()
        dirs = ['mesh_tools/source/']

        # pylint: disable=redefined-builtin
        for dir in dirs:
            grab_folder(self.config, src=self.lfric_core_root / dir,
                        dst_label='')

    def get_rose_meta(self):
        return (self.lfric_core_root / 'mesh_tools' / 'rose-meta' /
                'lfric-mesh_tools' / 'HEAD' / 'rose-meta.conf')


# -----------------------------------------------------------------------------
if __name__ == '__main__':

    logger = logging.getLogger('fab')
    logger.setLevel(logging.DEBUG)
    fab_mesh_tool = FabMeshTool(name="mesh_tools",
                                root_symbol=[
                                    'cubedsphere_mesh_generator',
                                    'planar_mesh_generator',
                                    'summarise_ugrid'])
    fab_mesh_tool.build()
