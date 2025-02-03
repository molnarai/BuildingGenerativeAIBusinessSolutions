#!/bin/bash

FREE_PORT=`ruby -e 'require "socket"; puts Addrinfo.tcp("", 0).bind {|s| s.local_address.ip_port }'`
CONTAINER_NAME="${USER}-pytorch-24"
PORT=${1:-$FREE_PORT}

cat <<"EOF"
  ____       _____              _       _          _     
 |  _ \ _   |_   _|__  _ __ ___| |__   | |    __ _| |__  
 | |_) | | | || |/ _ \| '__/ __| '_ \  | |   / _` | '_ \ 
 |  __/| |_| || | (_) | | | (__| | | | | |__| (_| | |_) |
 |_|    \__, ||_|\___/|_|  \___|_| |_| |_____\__,_|_.__/ 
        |___/                                            

EOF
cat <<EOF
JupyterLab is running on port ${PORT}

+------------------------------------------------------------------+
| Create an SSH tunnel on your local computer with                 |
|    $ ssh -fNL 8888:localhost:${PORT} ${USER}@10.230.100.240 |
+------------------------------------------------------------------+

You can access Jupyter Lab by visiting:
    http://localhost:8888

Look in the Jupter output below for your access token!

EOF

podman build -t $CONTAINER_NAME .
podman run --rm \
        -p ${PORT}:8888 \
        --device nvidia.com/gpu=3 \
        --security-opt=label=disable \
        -v $PWD:/workspace/local \
        -v /staging/users/${USER}:/staging \
        -v /data:/workspace/data \
	$CONTAINER_NAME jupyter-lab

cat <<EOF

Consider cleaning up your container images:
EOF

# podman system prune -a
echo "Done"
