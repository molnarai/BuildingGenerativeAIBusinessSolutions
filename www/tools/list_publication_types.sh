#!/bin/bash
HOME_DIR="`dirname $0`/.."
jq ".records[].type" < ${HOME_DIR}/_data/publications.json  | sort | uniq -c
