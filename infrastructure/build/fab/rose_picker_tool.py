#!/usr/bin/python3

'''This module contains a function that returns a working version of a
rose_picker tool. It can either be a version installed in the system,
or otherwise a checked-out version in the fab-workspace will be used.
If required, a version of rose_picker will be checked out.
'''

import logging
import os
from pathlib import Path
from typing import Optional

from fab.tools import Category, Tool, ToolRepository
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
        :returns bool: whether rose_picker works by running `rose_picker -help`.
        '''
        try:
            self.run(additional_parameters="-help")
        except RuntimeError:
            return False

        return True

    def run(self, *args, **kwargs) -> None:
        '''
        This wrapper adds the required PYTHONPATH, and passes all
        parameters through to the tool's run function.

        :param Tuple args: arguments to pass to rose picker
        :param Dict kwargs: arguments to pass to rose picker
        '''
        env = os.environ.copy()
        env["PYTHONPATH"] = (f"{env.get('PYTHONPATH', '')}:"
                             f"{self._pythonpath}")

        super().run(*args, **kwargs, env=env)


# =============================================================================
def get_rose_picker(tag: Optional[str] = "v2.0.0") -> RosePicker:
    '''
    Returns a Fab RosePicker tool. It can either be a version installed
    in the system, which is requested by setting tag to `system`, or a
    newly installed version via an FCM checkout. If there is already a
    checked-out version, it will be used (i.e. no repeated downloads are
    done).

    :param Optional[str] tag: either the tag in the repository to use,
        or 'system' to indicate to use a version installed in the system
    :returns RosePicker: a Fab RosePicker tool instance
    '''

    if tag.lower() == "system":
        # 'system' means to use a rose_picker installed in the system
        # (i.e. available without any path or adjustment of PYTHONPATH)
        return Tool("rose_picker", exec_name="rose_picker")

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


# =============================================================================
if __name__ == "__main__":
    '''
    A small test for getting the rose picker tool.'
    '''
    rose_picker = get_rose_picker("v2.0.0")
