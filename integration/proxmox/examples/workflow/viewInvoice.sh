#!/bin/sh

# set -x

INVOICE_TYPE_NAME="Invoice"
INVOICE_TYPE_VERSION=1

# echo ""
# echo ""
# echo "Rendering $INVOICE_TYPE_NAME $INVOICE_TYPE_VERSION"
# echo "---"
GFS_HOST=$HOST gfscli render $INVOICE_TYPE_NAME -i "$1"
# echo "---"
# echo ""
# echo ""
