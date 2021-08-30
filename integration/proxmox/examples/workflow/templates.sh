#!/bin/sh

# set -x

INVOICE_TEMPLATE_NAME="InvoiceTpl"

GFS_HOST=$HOST gfscli create template --data name=$INVOICE_TEMPLATE_NAME template="@./templates/invoice.template" --show id name template
