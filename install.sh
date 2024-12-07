#!/bin/bash

if [[ -z "$1" || -z "$2" ]]; then
	echo "Usage: install.sh PATH_TO_LFRIC_CORE PATH_TO_LFRIC_APPS"
	exit
fi

LFRIC_CORE=$1

LFRIC_APPS=$2

if [[ ! -d $LFRIC_CORE/infrastructure ]]; then
	echo "'$LFRIC_CORE' does not seem to be an LFRic_core checkout, can't find infrastructure."
	exit
fi

if [[ ! -d $LFRIC_APPS/applications ]]; then
	echo "'$LFRIC_APPS' does not seem to be an LFRic_apps checkout, can't find applications."
	exit
fi

# Copy the fab base class into the infrastructure build directory
cp -r infrastructure $LFRIC_CORE

# Copy the app build scripts into the applications directory
rsync -a applications $LFRIC_APPS --exclude applications/skeleton
cp -r applications/skeleton $LFRIC_CORE/applications
cp -r mesh_tools $LFRIC_CORE
cp build.sh $LFRIC_CORE
