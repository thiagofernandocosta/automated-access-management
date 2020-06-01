#!/bin/sh

source ./scripts/tools.sh
BASE_DIR=$(pwd)/tools/jira

pip install -r $BASE_DIR/requirements.txt
python $BASE_DIR/_jira.py $WORKFLOW