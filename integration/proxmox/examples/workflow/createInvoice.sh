#!/bin/sh

# set -x

INVOICE_NAME=$1
INVOICE_DESC=$2
INVOICE_AMT=$3

INVOICE_ID=`GFS_HOST=$HOST gfscli exec query @./queries/createInvoice.query --data name="$INVOICE_NAME" description="$INVOICE_DESC" amount="$INVOICE_AMT" | jq -j ".data.createInvoice.instance.id"`

# GFS_HOST=$HOST gfscli exec query @./queries/getInvoice.query --data name="$INVOICE_NAME"
# INVOICE_ID=`GFS_HOST=$HOST gfscli exec query @./queries/getInvoice.query --data name=$INVOICE_NAME | jq -j ".data.Invoices[0].id"`

INVOICE_TEMPLATE_NAME="InvoiceTpl"
INVOICE_TEMPLATE_ID=`GFS_HOST=$HOST gfscli query template --match name=$INVOICE_TEMPLATE_NAME --show id name | jq -j ".[0].id"`

GFS_HOST=$HOST gfscli link view --from "$INVOICE_ID" --to "$INVOICE_TEMPLATE_ID"

echo "Created a new invoice with id $INVOICE_ID"
echo "Please view it with: ./viewInvoice.sh \"${INVOICE_ID}\""
