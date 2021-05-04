#!/bin/bash
set -e

export GFS_NAMESPACE="gfs1"
export GFS_HOST="192.168.0.160"
export GFS_PORT="5000"
export GFS_USERNAME="root"
export GFS_PASSWORD="root"

export GRAPH_URL="http://$GFS_HOST:$GFS_PORT/api/v1.0/gfs1/graph"
export GRAPH_API_URL="http://$GFS_HOST:$GFS_PORT"

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
THIS_DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
source $THIS_DIR/settings.sh

# echo "Deleting Graph: curl -s -X 'DELETE' $GRAPH_URL"
# DELETE_RETVAL=$(curl -s -X "DELETE" $GRAPH_URL)
# echo "DELETE_RETVAL: $DELETE_RETVAL"

#########################################################
## Main Automation Pipeline
#########################################################

/usr/local/bin/gfscompose create \
  --host $GFS_HOST \
  --port $GFS_PORT \
  --namespace $GFS_NAMESPACE \
  --file $THIS_DIR/proxmox-compose.yml
# /usr/local/bin/gfscompose create --file $THIS_DIR/proxmox-compose2.yml
