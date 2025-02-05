#!/bin/bash
cat<<'EOF'
  ____                 _     ____                 _                                  _    
 |  _ \ ___  __ _  ___| |_  |  _ \  _____   _____| | ___  _ __  _ __ ___   ___ _ __ | |_  
 | |_) / _ \/ _` |/ __| __| | | | |/ _ \ \ / / _ \ |/ _ \| '_ \| '_ ` _ \ / _ \ '_ \| __| 
 |  _ <  __/ (_| | (__| |_  | |_| |  __/\ V /  __/ | (_) | |_) | | | | | |  __/ | | | |_  
 |_| \_\___|\__,_|\___|\__| |____/ \___| \_/ \___|_|\___/| .__/|_| |_| |_|\___|_| |_|\__| 
                                                         |_|                                                                                                                    
Locally run React Development Environment
EOF
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

# Check if the required environment variables are set


# check if podman or docker command is installed, define variable CONTAINERCMD
if [ -x "$(command -v podman)" ]; then
    CONTAINER_CMD=podman
    echo "podman found"
elif [ -x "$(command -v docker)" ]; then
    CONTAINER_CMD=docker
    echo "docker found"
else
    echo "Neither podman nor docker command found. Please install one of them."
    exit 1
fi

FRONTEND_DIR=`dirname $0`
APP_NAME=`basename $0 .sh`
CONTAINER_NAME="local/${USER}/${APP_NAME}"
echo "Container name: $CONTAINER_NAME"

# mkdir -p src/$APP_NAME
# OLLAMA_BASE_URL=${OLLAMA_BASE_URL:-XXXXXXXXXXXXXXXXXXXXXX}
# AI_APPLICATION_BASE_URL=${AI_APPLICATION_BASE_URL:-XXXXXXXXXXXXXXXXXXXXXX}
LOCAL_PORT=3000


if [ -z "$1" ]
then
    CMD="help"
else
    CMD=$1
fi

if [ ! -f  src/$APP_NAME/.env ]
then
    echo "Creating .env file"
    cat << EOF > src/$APP_NAME/.env
REACT_APP_OLLAMA_BASE_URL=${OLLAMA_BASE_URL}
REACT_APP_AI_APPLICATION_BASE_URL=${AI_APPLICATION_BASE_URL}
REACT_APP_AI_APPLICATION_NAME=${AI_APPLICATION_NAME:-$APP_NAME}
EOF
fi

case "$CMD" in 
    install)
        echo "Building container"
        $CONTAINER_CMD build -t $CONTAINER_NAME .
        ;;
    run)
        echo "Running container"
        shift
        $CONTAINER_CMD run -it --rm \
            -v "$FRONTEND_DIR/src:/app/src" \
            -w /app/src/$APP_NAME  \
            $CONTAINER_NAME $*
        ;;
    create)
        if [ -d "src/$APP_NAME" ]; then
            echo "Directory $APP_NAME already exists. Please remove it first."
            exit 1
        fi
        echo "Creating container image"
        $CONTAINER_CMD build -t $CONTAINER_NAME .

        # echo "Install React"
        # $CONTAINER_CMD run -it --rm \
        #     -v "$FRONTEND_DIR/src:/app/src" \
        #     -w /app/src \
        #     $CONTAINER_NAME npm install

        echo "Creating Application"
        $CONTAINER_CMD run -it --rm \
            -v "$FRONTEND_DIR/src:/app/src" \
            -w /app/src \
            $CONTAINER_NAME npx create-react-app $APP_NAME

        echo "Installing dependencies"
        $CONTAINER_CMD run -it --rm \
            -v "$FRONTEND_DIR/src:/app/src" \
            -w /app/src/$APP_NAME  \
            $CONTAINER_NAME npm install axios react-router-dom

        echo "Create .env file"
        cat << EOF > src/$APP_NAME/.env
REACT_APP_OLLAMA_BASE_URL=${OLLAMA_BASE_URL}
REACT_APP_AI_APPLICATION_BASE_URL=${AI_APPLICATION_BASE_URL}
REACT_APP_AI_APPLICATION_NAME=${AI_APPLICATION_NAME:-$APP_NAME}
EOF
        echo "done."
        ;;
    build)
        echo "Build static React app"
        $CONTAINER_CMD run --rm \
            -v "$FRONTEND_DIR/src:/app/src" \
            -w /app/src/$APP_NAME  \
            $CONTAINER_NAME npm install
        $CONTAINER_CMD run --rm \
            -v "$FRONTEND_DIR/src:/app/src" \
            -w /app/src/$APP_NAME  \
            $CONTAINER_NAME npm run build 
        ;;
    start)
        echo "Starting container"
        $CONTAINER_CMD run -it --rm \
            -p $LOCAL_PORT:3000 \
            -v "$FRONTEND_DIR/src:/app/src" \
            -w /app/src/$APP_NAME \
            $CONTAINER_NAME npm start 
        ;;
    *)
        cat<<EOF
Usage: $0 [install|run|create|build|start]"

install: Build the container image
run:     Run the container in interactive mode
create:  Create a new React application with the name $APP_NAME
build:   Build the React application
start:   Start the React application in development mode

EOF
        exit 1
        ;;
esac
echo "done."


