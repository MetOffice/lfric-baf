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

## TODO:
Support building Jules from a local directory instead
of a checkout.
