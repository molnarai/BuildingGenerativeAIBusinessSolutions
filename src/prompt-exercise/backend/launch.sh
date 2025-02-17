#!/bin/bash
cat<<'EOT'
  ____             _                  _   ____                  _               
 | __ )  __ _  ___| | _____ _ __   __| | / ___|  ___ _ ____   _(_) ___ ___  ___ 
 |  _ \ / _` |/ __| |/ / _ \ '_ \ / _` | \___ \ / _ \ '__\ \ / / |/ __/ _ \/ __|
 | |_) | (_| | (__|   <  __/ | | | (_| |  ___) |  __/ |   \ V /| | (_|  __/\__ \
 |____/ \__,_|\___|_|\_\___|_| |_|\__,_| |____/ \___|_|    \_/ |_|\___\___||___/
                                                                                
EOT
# Copyright (c) 2025 Péter Molnár
# LinkedIn: https://www.linkedin.com/in/petermolnar/
#
# This code is licensed under the Creative Commons license. 
# You are free to use, modify, and distribute it as long as proper attribution is provided.
# 
# Authorship: Péter Molnár with assistance from AI tools.
# 
# Disclaimer: This code is provided "as is", without any guarantees of correctness or functionality.
# Use it at your own risk. The author assumes no liability for any issues arising from its use.
#

# Test if docker or podman is installed, define variable COMPOSE with the respctive command
if command -v podman &> /dev/null
then
    COMPOSE="podman compose"
    CMD="podman"
elif command -v docker &> /dev/null
then
    COMPOSE="docker compose"
    CMD="docker"

else
    echo "Neither docker nor podman is installed."
    exit 1
fi


function title() {
    local TITLE=$1
    if command -v figlet &> /dev/null
    then
        figlet -r -f small "$TITLE"
    else
        echo "*************************************************************"
        echo "******    $TITLE"
        echo "*************************************************************"
    fi
}


BACKEND_ROOT=`dirname $0`
BACKEND_ROOT=$(realpath $BACKEND_ROOT)
if [ -f $BACKEND_ROOT/../.env ]
then
    echo "Loading environment variables from .env file..."
    cat<<'EOT' > $BACKEND_ROOT/.env
########################################################################
####                                                                ####
#### Do not edit: this file is created by the configuration script. ####
####                                                                ####
########################################################################
EOT
 
    (source $BACKEND_ROOT/../.env ; printenv | awk -F'=' '{st = index($0, "="); print "export " $1 "=\"" substr($0,st+1) "\""}' | sort >>  $BACKEND_ROOT/.env)
    source $BACKEND_ROOT/.env
else
    echo "No .env file found. Please run $0 localconf"
    exit 1
fi


echo "Project: $PROJECT"
echo "Environment: $ENVIRONMENT"
echo "Project data directory: $PROJECT_DATA_DIR"


ACTION=${1:-help}
shift

# Switch to main dir
pushd $BACKEND_ROOT > /dev/null
case $ACTION in
    help)
        echo "Usage: $0 [build|start|stop|status|localconf]"
        exit 0
        ;;
    build)
        title Build
        echo "Creating directories..."
        mkdir -p $PROJECT_DATA_DIR/$PROJECT/$ENVIRONMENT/{postgres,rabbitmq,elasticsearch,elasticsearch-tmp,metabase}
        # ls -l $PROJECT_DATA_DIR/$PROJECT/$ENVIRONMENT
        echo "Buidling container images..."
        $COMPOSE build
        ;;
    start)
        title Start
        echo "Starting the services..."
        $COMPOSE up -d
        ;;
    stop)
        title Stop
        echo "Stopping the services..."
        $COMPOSE down
        ;;
    status)
        title Status
        echo "Checking the status of the services..."
        $COMPOSE ps
        ;;
    log*)
        title Logs
        echo "Checking the status of the services..."
        $COMPOSE logs -f $*
        ;;
    *)
        echo "Invalid action: $ACTION"
        exit 1
        ;;
esac
popd > /dev/null
