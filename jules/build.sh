#! /usr/bin/bash

if [ -z $1 ]; then
	echo "build.sh Fab_script"
	exit
fi

# This script initialised PYTHONPATH to make the required
# base class accessible to all script.
# It takes one parameters: the name of a (python) script
ROOT_DIR=$( cd -- "$( dirname -- "$(readlink -f ${BASH_SOURCE[0]})" )" &> /dev/null && pwd )

echo "ROOT $ROOT_DIR"
FAB_DIR=$ROOT_DIR/../infrastructure/build/fab
PSYCLONE_BUILD_DIR=$ROOT_DIR/infrastructure/build/psyclone

# Add ROOT_DIR here first, so we import compiler settings from
# THIS default directory
PYTHONPATH=$ROOT_DIR:$FAB_DIR:$PSYCLONE_BUILD_DIR:$PYTHONPATH $*
