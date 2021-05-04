#!/bin/bash

export GFS_NAMESPACE="gfs1"
export GFS_HOST="192.168.0.160"
# export GFS_HOST="localhost"
export GFS_PORT="5000"
export GFS_USERNAME="root"
export GFS_PASSWORD="root"

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
BOTSNODE_NAME='botnode56355'
BOTSNODE_ID='60'
echo "Default: Creating ${BOTSNODE_NAME}"
# BOTSNODE_ID=$(GFS_HOST=$HOST gfscli create $MACHINE_TYPE_NAME --data name=$BOTSNODE_NAME arch=i386 --show id name | jq -j .instance.id)
echo "gfscli create Machine -i $BOTSNODE_ID --data name=$BOTSNODE_NAME arch=x86_64 memory=4096 cpus=2 cores=2 ht=yes --show id name
"
gfscli update Machine -i $BOTSNODE_ID --data name=$BOTSNODE_NAME arch=x86_64 memory=4096 cpus=2 cores=2 ht=yes --show id name
