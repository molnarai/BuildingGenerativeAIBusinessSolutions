#!/bin/bash
WWW_DIR="$(dirname $0)/.."
WEB_SERVER="10.230.100.202"
BASE_URL="http://www.insight.gsu.edu/MSA8700"
WEB_USER="insight"
WEB_HTML_DIR="/var/www/html/MSA8700"
cat<<'EOF'
  ____           _                  __        __   _       ____                           
 |  _ \ ___  ___| |_    ___  _ __   \ \      / /__| |__   / ___|  ___ _ ____   _____ _ __ 
 | |_) / _ \/ __| __|  / _ \| '_ \   \ \ /\ / / _ \ '_ \  \___ \ / _ \ '__\ \ / / _ \ '__|
 |  __/ (_) \__ \ |_  | (_) | | | |   \ V  V /  __/ |_) |  ___) |  __/ |   \ V /  __/ |   
 |_|   \___/|___/\__|  \___/|_| |_|    \_/\_/ \___|_.__/  |____/ \___|_|    \_/ \___|_|   
                                                                                          
Uploading...

EOF
pushd $WWW_DIR
hugo --gc --minify --baseURL ${BASE_URL}
scp -r public/* ${WEB_USER}@${WEB_SERVER}:${WEB_HTML_DIR}/
echo "Done."
popd

