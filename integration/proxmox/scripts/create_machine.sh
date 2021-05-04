#!/bin/bash

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
THIS_DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
source $THIS_DIR/settings.sh

# MACHINE_TYPE_NAME="ProxmoxMachine"
MACHINE_TYPE_NAME="Machine"
# NODE_NAME='botnode'$((1 + $RANDOM % 10000))

# gfscli create $MACHINE_TYPE_NAME --data \
#     name=$NODE_NAME \
#     arch=x86_64 \
#     memory=4096 \
#     cpus=2 \
#     ht=true \
#     cores=2 \
#     diskController0=VirtIOSCSI \
#     diskDevice0=somedisk \
#     --show \
#     id \
#     name

# gfscli create $MACHINE_TYPE_NAME --data \
#     name=$NODE_NAME \
#     arch=x86_64 \
#     memory=4096 \
#     cpus=2 \
#     cores=2 \
#     --show \
#     id \
#     name

# BOTSNODE_NAME='botnode'$((1 + $RANDOM % 10000))
BOTSNODE_NAME='botnode5633'
BOTSNODE_ID='60'
echo "Default: Creating ${BOTSNODE_NAME}"
# BOTSNODE_ID=$(GFS_HOST=$HOST gfscli create $MACHINE_TYPE_NAME --data name=$BOTSNODE_NAME arch=i386 --show id name | jq -j .instance.id)
echo "gfscli create $MACHINE_TYPE_NAME --data name=$BOTSNODE_NAME arch=x86_64 memory=4096 cpus=2 cores=2 ht=yes --show id name"
gfscli create $MACHINE_TYPE_NAME --data name=$BOTSNODE_NAME arch=x86_64 memory=4096 cpus=2 cores=2 ht=yes --show id name
