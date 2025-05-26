# Jules
This directory contains a simple build script that allows using BAF
to build a Jules executable

## Installation
Clone the BAF repository. Install the included Fab version using:

    pip install --user ./fab

Setup the environment variable ``FAB_WORKSPACE`` to point to
a suitable location to build Jules in. Then run the script
with the provided ``build.sh`` script. The script will setup
the ``PYTHONPATH`` environment to make sure the required
BAF script will be found, and then build Jules.

Besides the command line options supported by BAF,
it accepts the option ``--revision`` to specify the
Jules version to check out. It defaults to ``vn7.8``.

The compiler setup is taken from the ``default`` directory.
Note that at this stage only the gnu setup has been verified
to work with Jules, see ticket #47.

## TODO:
1. Support building Jules from a local directory instead
   of a checkout.
2. Verify (and fix if required) the build with other compilers,
   see https://github.com/MetOffice/lfric-baf/issues/47.
2. Move the Jules build into the Jules trunk, e.g. into
   main/trunk/etc/fab.
