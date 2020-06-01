#!/bin/sh

source ./scripts/tools.sh
BASE_DIR=$(pwd)/tools/kubernetes

if [ "$WORKFLOW" = "apply" ]; then
    print_logs "Granting permission to $EMAIL on Kubernetes cluster"
    kubectl create rolebinding "${EMAIL%@*}" --role=user-readonly --user=$EMAIL -n default || true
    python $BASE_DIR/_kube.py
else
    print_logs "Removing Permissions from $EMAIL on kubernetes cluster"
    kubectl delete rolebinding "${EMAIL%@*}" -n default || true
fi