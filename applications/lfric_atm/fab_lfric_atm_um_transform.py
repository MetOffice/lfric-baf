#!/usr/bin/env python3
# ##############################################################################
#  (c) Crown copyright Met Office. All rights reserved.
#  For further details please refer to the file COPYRIGHT
#  which you should have received as part of this distribution
# ##############################################################################

'''A FAB build script for lfric_atm. It relies on the LFRicBase class
contained in the infrastructure directory.
'''

import logging

from fab.artefacts import ArtefactSet
from fab.tools import Category

from fab_lfric_atm import FabLFRicAtm


class FabLFRicAtmUmTransform(FabLFRicAtm):
    '''An lfric_atm build script that additional shows how to call
    PSyclone with a transformation script for existing Fortran code.
    '''

    def get_um_script(self, input_file, config):
        ''':returns: the PSyclone script to be used for the specified
            input file. ATM this always returns the same script.
            See lfric_base.get_transformation_script for a more
            elaborate example.
        '''
        return config.source_root / "optimisation" / "umscript.py"

    def psyclone(self):
        super().psyclone()

        psyclone = self.config.tool_box[Category.PSYCLONE]
        psyclone_cli_args = self.get_psyclone_config()
        # Long term we would want to run these in parallel, but for
        # now this version is easy to understand. Add more files
        # as required to the loop. Note that the files are already
        # preprocessed at this stage, so make sure not to use capital
        # F90!
        for file in ["science/um/atmosphere/boundary_layer/bdy_impl3.f90"]:
            file_path = self.config.build_output / file
            # Make up a new output filename
            transformed_file = file_path.with_stem(file_path.stem +
                                                   "_psyclonified")
            psyclone.process(config=self.config,
                             x90_file=file_path,
                             api=None,     # This triggers transformation only
                             transformed_file=transformed_file,
                             transformation_script=self.get_um_script,
                             additional_parameters=psyclone_cli_args)
            # Now remove the unprocessed file from the build files, and add
            # the newly file processed file
            self.config.artefact_store.replace(ArtefactSet.FORTRAN_BUILD_FILES,
                                               [file_path],
                                               [transformed_file])


# -----------------------------------------------------------------------------
if __name__ == '__main__':

    logger = logging.getLogger('fab')
    logger.setLevel(logging.DEBUG)
    # Give the build directory a different name,
    # but the binary remains lfric_atm
    fab_lfric_atm_um = FabLFRicAtmUmTransform(name="lfric_atm_um_transform",
                                              root_symbol="lfric_atm")
    fab_lfric_atm_um.build()
