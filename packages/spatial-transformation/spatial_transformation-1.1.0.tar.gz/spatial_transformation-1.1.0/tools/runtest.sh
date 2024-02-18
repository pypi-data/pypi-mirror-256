#!/bin/bash

# use with
# > bash runtest.sh
#
# or specify marker with
# > bash runtest.sh MARKERNAME
#
# possible markers are:
# - randomized
# - hardcoded

# read marker name if set, else use no marker ------------------------------------------
PARAM_MARKER=""
if [ -z ${1+x} ]; then PARAM_MARKER=$1; else PARAM_MARKER=" -m $1"; fi

# do test ------------------------------------------------------------------------------
pytest --cov-report html:htmlcov --cov . 'tests/' $PARAM_MARKER
