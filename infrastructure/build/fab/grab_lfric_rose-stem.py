#!/usr/bin/env python3
# ##############################################################################
#  (c) Crown copyright Met Office. All rights reserved.
#  For further details please refer to the file COPYRIGHT
#  which you should have received as part of this distribution
# ##############################################################################

import os

from pathlib import Path

from fab.build_config import BuildConfig
from fab.steps.grab.fcm import fcm_export
from fab.tools import ToolBox

fab_workspace = Path(os.getenv("SOURCE_ROOT"))

lfric_core_source_config = BuildConfig(
    project_label='grab_lfric_source', tool_box=ToolBox(),
    fab_workspace=fab_workspace)
lfric_apps_source_config = BuildConfig(
    project_label='grab_lfric_source', tool_box=ToolBox(),
    fab_workspace=fab_workspace)

if __name__ == '__main__':

    with lfric_core_source_config:
        fcm_export(
            lfric_core_source_config, src=os.getenv("SOURCE_LFRIC_CORE"),
            dst_label='core')

    with lfric_apps_source_config:
        fcm_export(
            lfric_apps_source_config, src=os.getenv("SOURCE_LFRIC_APPS"),
            dst_label='apps')
