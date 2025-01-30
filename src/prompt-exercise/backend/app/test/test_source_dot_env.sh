#!/bin/bash
# Unless required by applicable law or agreed to in writing, software
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
set -e
BASE_DIR=$(dirname $0)/../..
echo "======================================================"
echo "Using base directory: `realpath $BASE_DIR`"
echo "======================================================"
if [ ! -f $BASE_DIR/.env ]; then
  echo "Please create a .env file in the project root directory."
  exit 1
fi
cat $BASE_DIR/.env | grep -v '^#' | sort
echo
echo "======================================================"
(source $BASE_DIR/.env ; printenv | sort)
echo "======================================================"


