##############################################################################
# (c) Crown copyright Met Office. All rights reserved.
# The file LICENCE, distributed with this code, contains details of the terms
# under which the code may be used.
##############################################################################
# Author J. Henrichs, Bureau of Meteorology
# Author J. Lyu, Bureau of Meteorology

"""
This module contains a function that returns a working version of a
rose_picker tool. It can either be a version installed in the system,
or otherwise a checked-out version in the fab-workspace will be used.
If required, a version of rose_picker will be checked out.
"""

import logging
import os
from pathlib import Path
import shutil
from typing import cast, List, Union

from fab.api import Category, Tool, ToolRepository
from fab.tools.versioning import Fcm
from fab.util import get_fab_workspace

logger = logging.getLogger('fab')


class RosePicker(Tool):
    '''This implements rose_picker as a Fab tool. It supports dynamically
    adding the required PYTHONPATH to the environment in case that rose_picker
    is not installed, but downloaded.

    :param Path path: the path to the rose picker binary.
    '''
    def __init__(self, path: Path):
        super().__init__("rose_picker", exec_name=str(path))
        # This is the required PYTHONPATH for running rose_picker
        # when it is installed from the repository:
        self._pythonpath = path.parents[1] / "lib" / "python"

    def check_available(self) -> bool:
        '''
        :returns bool: whether rose_picker works by running
            `rose_picker -help`.
        '''
        try:
            self.run(additional_parameters="-help")
        except RuntimeError:
            return False

        return True

    def execute(self, parameters: List[Union[Path, str]]) -> None:
        '''
        This wrapper adds the required PYTHONPATH, and passes all
        parameters through to the tool's run function.

        :param additional_parameter: A list of parameters for rose picker.
        '''
        env = os.environ.copy()
        env["PYTHONPATH"] = (f"{env.get('PYTHONPATH', '')}:"
                             f"{self._pythonpath}")

        self.run(additional_parameters=parameters, env=env)


# =============================================================================
def get_rose_picker(tag: str = "v2.0.0") -> RosePicker:
    '''
    Returns a Fab RosePicker tool. It can either be a version installed
    in the system, which is requested by setting tag to `system`, or a
    newly installed version via an FCM checkout. If there is already a
    checked-out version, it will be used (i.e. no repeated downloads are
    done).

    :param tag: Either the tag in the repository to use,
        or 'system' to indicate to use a version installed in the system.

    :returns RosePicker: a Fab RosePicker tool instance
    '''

    if tag.lower() == "system":
        # 'system' means to use a rose_picker installed in the system
        which_rose_picker = shutil.which("rose_picker")
        if not which_rose_picker:
            raise RuntimeError("Cannot find system rose_picker tool.")
        return RosePicker(Path(which_rose_picker))

    # Otherwise use rose_picker from the default Fab workspace. It will
    # create a instance of the class above, which will add its path to
    # PYTHONPATH when executing a rose_picker command.

    gpl_utils = get_fab_workspace() / f"gpl-utils-{tag}" / "source"
    rp_path = gpl_utils / "bin" / "rose_picker"
    rp = RosePicker(rp_path)

    # If the tool is not available (the class will run `rose_picker -help`
    # to verify this ), install it
    if not rp.is_available:
        fcm = ToolRepository().get_default(Category.FCM)
        fcm = cast(Fcm, fcm)
        # TODO: atm we are using fcm for the checkout, because using FCM
        # keywords is more portable. We cannot use a Fab config (since this
        # function is called from within a Fab build), so that means the
        # gpl-utils-* directories in the Fab workspace directories do not
        # have the normal directory layout.
        logger.info(f"Installing rose_picker tag '{tag}'.")
        fcm.checkout(src=f'fcm:lfric_gpl_utils.x/tags/{tag}',
                     dst=gpl_utils)

        # We need to create a new instance, since `is_available` is
        # cached (I.e. it's always false in the previous instance)
        rp = RosePicker(rp_path)

    if not rp.is_available:
        msg = f"Cannot run rose_picker tag '{tag}'."
        logger.exception(msg)
        raise RuntimeError(msg)
    return rp
