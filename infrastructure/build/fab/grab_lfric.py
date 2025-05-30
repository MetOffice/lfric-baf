#!/usr/bin/env python3
# ##############################################################################
#  (c) Crown copyright Met Office. All rights reserved.
#  For further details please refer to the file COPYRIGHT
#  which you should have received as part of this distribution
# ##############################################################################

"""
This script is used on NCI GADI to export the LFRic core and apps codes
into the FAB workspace with FCM for Gitlab pipeline tests. 
"""

import sys

from fab.build_config import BuildConfig
from fab.steps.grab.fcm import fcm_export
from fab.steps.grab.folder import grab_folder
from fab.tools import ToolBox
from fab.util import get_fab_workspace

fab_workspace = get_fab_workspace()

lfric_core_rev_file = fab_workspace / 'lfric_core_revision'
lfric_apps_rev_file = fab_workspace / 'lfric_apps_revision'

with open(lfric_core_rev_file, 'r') as file:
    LFRIC_CORE_REVISION = file.readline().strip('\n')
print('lfric core revision: ' + LFRIC_CORE_REVISION)

with open(lfric_apps_rev_file, 'r') as file:
    LFRIC_APPS_REVISION = file.readline().strip('\n')
print('lfric apps revision: ' + LFRIC_APPS_REVISION)

ROSE_PICKER_REVISION = LFRIC_CORE_REVISION

print('lfric core revision: ' + LFRIC_CORE_REVISION)
print('rose-picker revision: ' + ROSE_PICKER_REVISION)

# these configs are interrogated by the build scripts
# todo: doesn't need two separate configs, they use the same project workspace
lfric_core_source_config = BuildConfig(
    project_label=f'lfric source {LFRIC_CORE_REVISION}', tool_box=ToolBox(),
    mpi=False, openmp=False,
    )
lfric_apps_source_config = BuildConfig(
    project_label=f'lfric source {LFRIC_CORE_REVISION}', tool_box=ToolBox(),
    mpi=False, openmp=False,
    )

if __name__ == '__main__':

    if len(sys.argv) > 1:
        with lfric_core_source_config:
            grab_folder(lfric_core_source_config, src=sys.argv[1])

    else:
        with lfric_core_source_config:
            fcm_export(
                lfric_core_source_config, src='fcm:lfric.xm_tr',
                revision=LFRIC_CORE_REVISION, dst_label='core')

        with lfric_apps_source_config:
            fcm_export(
                lfric_apps_source_config, src='fcm:lfric_apps.xm_tr',
                revision=LFRIC_APPS_REVISION, dst_label='apps')
