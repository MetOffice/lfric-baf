#! /usr/bin/bash

if [ -z $1 ]; then
	echo "build.sh Fab_script"
	exit
fi

# This script initialised PYTHONPATH to make the required
# base class accessible to all script.
# It takes one parameters: the name of a (python) script
ROOT_DIR=$( cd -- "$( dirname -- "$(readlink -f ${BASH_SOURCE[0]})" )" &> /dev/null && pwd )

# Make sure that this script is indeed started from
# lfric-core (and not e.g. from the baf directory)
if [[ ! -d $ROOT_DIR/components ]]; then
        echo "'$ROOT_DIR' does not seem to be an LFRic_core checkout, can't find components."
        exit
fi

FAB_DIR=$ROOT_DIR/infrastructure/build/fab
FAB_SUBMODULE_DIR=$ROOT_DIR/fab/source
PSYCLONE_BUILD_DIR=$ROOT_DIR/infrastructure/build/psyclone

PYTHONPATH=$FAB_DIR:$FAB_SUBMODULE_DIR:$PSYCLONE_BUILD_DIR:$PYTHONPATH $*
