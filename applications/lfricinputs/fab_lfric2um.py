#!/usr/bin/env python3
# ##############################################################################
#  (c) Crown copyright Met Office. All rights reserved.
#  For further details please refer to the file COPYRIGHT
#  which you should have received as part of this distribution
# ##############################################################################

'''A FAB build script for lfricinputs-lfric2um. It relies on
the FabLfricInputs class contained in fab_lfricinputs.py.
'''

import logging

from fab_lfricinputs import FabLfricInputs


# -----------------------------------------------------------------------------
if __name__ == '__main__':

    logger = logging.getLogger('fab')
    logger.setLevel(logging.DEBUG)
    fab_lfric_inputs = FabLfricInputs(name="lfric_inputs",
                                      root_symbol="lfric2um")
    fab_lfric_inputs.build()
