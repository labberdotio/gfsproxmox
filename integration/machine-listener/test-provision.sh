#!/bin/bash

API_NODE="192.168.0.180"
TARGET_NODE="botcore"

AUTH_Cookie=$(curl --silent --insecure --data "username=bots@pam&password=bots123" \
    https://$API_NODE:8006/api2/json/access/ticket \
    | jq --raw-output '.data.ticket' | sed 's/^/PVEAuthCookie=/')

CSRF_Token=$(curl --silent --insecure --data "username=bots@pam&password=bots123" \
    https://$API_NODE:8006/api2/json/access/ticket \
    | jq --raw-output '.data.CSRFPreventionToken' | sed 's/^/CSRFPreventionToken:/')

# curl  --insecure --cookie $AUTH_Cookie https://$API_NODE:8006/api2/json/nodes/$TARGET_NODE/status

curl --silent --insecure --cookie $AUTH_Cookie https://$API_NODE:8006/api2/json/nodes/botcore/qemu | jq '.'
