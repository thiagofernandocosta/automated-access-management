#!/bin/sh

source ./scripts/tools.sh
BASE_DIR=$(pwd)/tools/git

pip install -r $BASE_DIR/requirements.txt
python $BASE_DIR/_git.py $WORKFLOW