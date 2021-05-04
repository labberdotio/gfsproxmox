#!/bin/bash
set -e

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
THIS_DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
source $THIS_DIR/settings.sh

#########################################################
## Main Automation Pipeline
#########################################################

$THIS_DIR/../../system/controller/gfs/do-compose.sh

/usr/local/bin/gfscompose create \
  --host $GFS_HOST \
  --port $GFS_PORT \
  --namespace $GFS_NAMESPACE \
  --file $THIS_DIR/proxmox-compose.yml
# /usr/local/bin/gfscompose create --file $THIS_DIR/proxmox-compose2.yml
