#!/usr/bin/env python3
# ##############################################################################
#  (c) Crown copyright Met Office. All rights reserved.
#  For further details please refer to the file COPYRIGHT
#  which you should have received as part of this distribution
# ##############################################################################

'''A FAB build script for lfric_atm that supports extraction. It relies on the
FAB base class for LFRic ATM and the extraction mixin class,.
'''

from fab_lfric_atm import FabLFRicAtm
from extract_mixin import ExtractMixin


class FabLFRicAtmExtract(ExtractMixin, FabLFRicAtm):
    '''This trivial class implements extraction for LFRic-ATM. The mixin
    Extract class overwrites the psyclone step (to insert its own
    step of removing private declarations first).

    There is no implementation here needed otherwise. The mixing inserts
    the required phases, and overwrites the method with which to determine
    the PSyclone script to use.

    The only other important part here is __main__, which sets a different
    fab workspace-name (and uses the class here).
    '''


# -----------------------------------------------------------------------------
if __name__ == '__main__':

    fab_lfric_atm = FabLFRicAtmExtract(name="lfric_atm_extract",
                                       root_symbol="lfric_atm")
    fab_lfric_atm.build()
