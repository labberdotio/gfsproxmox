#!/bin/sh

# set -x

GFS_HOST=$HOST gfscli exec query @./queries/getInvoice.query --data id=$1
