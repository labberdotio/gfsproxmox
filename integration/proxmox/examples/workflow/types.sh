#!/bin/sh

# set -x

INVOICE_TYPE_NAME="Invoice"
INVOICE_TYPE_VERSION=1

APPROVAL_TYPE_NAME="Approval"
APPROVAL_TYPE_VERSION=1

REVIEW_TYPE_NAME="Review"
REVIEW_TYPE_VERSION=1

GFS_HOST=$HOST gfscli create type $INVOICE_TYPE_NAME --version $INVOICE_TYPE_VERSION --property name=string description=string amount=string status=string --required name description amount --show name version | jq -j .instance.name
echo "Created new type $INVOICE_TYPE_NAME"
GFS_HOST=$HOST gfscli get type $INVOICE_TYPE_NAME --show name version

GFS_HOST=$HOST gfscli create type $APPROVAL_TYPE_NAME --version $APPROVAL_TYPE_VERSION --property status=string notice=string approver=string --required status notice approver --show name version | jq -j .instance.name
echo "Created new type $APPROVAL_TYPE_NAME"
GFS_HOST=$HOST gfscli get type $APPROVAL_TYPE_NAME --show name version

GFS_HOST=$HOST gfscli create type $REVIEW_TYPE_NAME --version $REVIEW_TYPE_VERSION --property status=string notice=string reviewer=string --required status notice reviewer --show name version | jq -j .instance.name
echo "Created new type $REVIEW_TYPE_NAME"
GFS_HOST=$HOST gfscli get type $REVIEW_TYPE_NAME --show name version

# gfscli query type --show name version

GFS_HOST=$HOST gfscli link approvalOf --from type $APPROVAL_TYPE_NAME $APPROVAL_TYPE_VERSION --to type $INVOICE_TYPE_NAME $INVOICE_TYPE_VERSION
echo "Created dependency approvalOf from $APPROVAL_TYPE_NAME to $INVOICE_TYPE_NAME"

GFS_HOST=$HOST gfscli link reviewOf --from type $REVIEW_TYPE_NAME $REVIEW_TYPE_VERSION --to type $APPROVAL_TYPE_NAME $APPROVAL_TYPE_VERSION
echo "Created dependency reviewOf from $REVIEW_TYPE_NAME to $APPROVAL_TYPE_NAME"
