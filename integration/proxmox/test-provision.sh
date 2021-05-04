#!/bin/bash

API_NODE="192.168.0.180"
TARGET_NODE="botcore"
TOKEN_ID='bots@pam!botstoken'
TOKEN_SECRET='2b29934d-d95e-48e4-9050-f3df9a083c5b'
REMOTE_NODE_ENDPOINT="https://$API_NODE:8006/api2/json/nodes/$TARGET_NODE"

echo "Authorization: PVEAPIToken=${TOKEN_ID}=${TOKEN_SECRET}"

curl --location --insecure --header "Authorization: PVEAPIToken=${TOKEN_ID}=${TOKEN_SECRET}" \
    --request GET $REMOTE_NODE_ENDPOINT
