#!/bin/sh

source ./scripts/tools.sh
BASE_DIR=$(pwd)/tools/slack

pip install -r $BASE_DIR/requirements.txt
python $BASE_DIR/_slack.py $WORKFLOW