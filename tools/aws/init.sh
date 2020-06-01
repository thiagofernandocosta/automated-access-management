#!/bin/sh

source ./scripts/tools.sh
BASE_DIR=$(pwd)/tools/aws

pip install -r $BASE_DIR/requirements.txt
python $BASE_DIR/_iam.py $WORKFLOW
python $BASE_DIR/_ses.py $WORKFLOW