##############################################################################
# Copyright (c) 2017,  Met Office, on behalf of HMSO and Queen's Printer
# For further details please refer to the file LICENCE.original which you
# should have received as part of this distribution.
##############################################################################


'''
PSyclone transformation script for the LFRic (Dynamo0p3) API to apply
colouring, OpenMP and redundant computation to the level-1 halo for
the initialisation built-ins generically.

'''

from psyclone_tools import (redundant_computation_setval, colour_loops,
                            openmp_parallelise_loops,
                            view_transformed_schedule)
from psyclone.domain.lfric import LFRicConstants, LFRicLoop
from psyclone.domain.lfric.transformations import LFRicExtractTrans


def trans(psy):
    '''
    Applies PSyclone colouring, OpenMP and redundant computation
    transformations.

    '''
    extract = LFRicExtractTrans()
    redundant_computation_setval(psy)
    # colour_loops(psy)
    # openmp_parallelise_loops(psy)
    view_transformed_schedule(psy)
    for invoke in psy.invokes.invoke_list:
        schedule = invoke.schedule
        for kern in schedule.walk(LFRicLoop):
            try:
                extract.apply(kern, {"create_driver": True})
            except NotImplementedError:
                pass
