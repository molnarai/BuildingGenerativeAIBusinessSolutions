#!/bin/bash
HOME_DIR="`dirname $0`/.."
BIBTEX2JSON="${HOME_DIR}/scripts/bibtex2bibjson.py"
ASSETS_DIR="${HOME_DIR}/assets"
DATA_DIR="${HOME_DIR}/_data"

${BIBTEX2JSON} ${ASSETS_DIR}/publications.bib > ${DATA_DIR}/publications.json
