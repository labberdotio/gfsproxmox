#!/bin/bash

MACHINE_TYPE_NAME="Machine"

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
THIS_DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
source $THIS_DIR/settings.sh

echo "$PMOXAPI_TOKEN"
MACHINE_ID=$(gfscli list $MACHINE_TYPE_NAME --show id, name | \
    jq -c '[.[] | select(.name | contains("botnode"))][0]' | \
    jq '.id' | \
    sed 's/"//g')

echo "MACHINE_ID: ${MACHINE_ID}"
gfscli delete $MACHINE_TYPE_NAME $MACHINE_ID
