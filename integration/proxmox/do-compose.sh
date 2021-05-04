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

# echo "Deleting Graph: curl -s -X 'DELETE' $GRAPH_URL"
# DELETE_RETVAL=$(curl -s -X "DELETE" $GRAPH_URL)
# echo "DELETE_RETVAL: $DELETE_RETVAL"

# TYPES_FILE="./autonomic-compose-types.yml"
# INSTANCES_FILE="./autonomic-compose-instances.yml"
# LINKS_FILE="./autonomic-compose-links.yml"
# echo "Running $TYPES_FILE"
# gfscli create --file ./autonomic-compose-types.yml
# echo "Running $INSTANCES_FILE"
# gfscli create --file ./autonomic-compose-instances.yml
# echo "Running $LINKS_FILE"
# gfscli create --file ./autonomic-compose-links.yml

#gfscli create --file ./autonomic-compose.yml
# gfscli create --file ./sample.yml
# gfscli create --file ./test-compose.yml

/usr/local/bin/gfscompose create --file $THIS_DIR/proxmox-compose.yml
# gfscli create --file ./sample.yml
# gfscli create --file ./test-compose.yml


# function finish {
#   popd
# }
# trap finish EXIT