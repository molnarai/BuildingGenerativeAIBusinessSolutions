#!/bin/bash
cat <<'EOT'
  _                           _              ___        
 | |    __ _ _   _ _ __   ___| |__    _ __  ( _ ) _ __  
 | |   / _` | | | | '_ \ / __| '_ \  | '_ \ / _ \| '_ \ 
 | |__| (_| | |_| | | | | (__| | | | | | | | (_) | | | |
 |_____\__,_|\__,_|_| |_|\___|_| |_| |_| |_|\___/|_| |_|
                                                        
EOT
# Launch script for n8n container.
ACTION=${1:-help}
shift

WORK_DIR=$(realpath $(dirname "$0")/..)/n8n-experiments-system-store
DATA_DIR=$(realpath $(dirname "$0")/..)/n8n-experiments-data
echo "Working directory: $WORK_DIR"
mkdir -p $WORK_DIR

BASE_PORT=23010

SERVER_IP='localhost'
UID=$(id -u)
GID=$(id -g)

CONTAINER_NAME="${USER}-n8n-experiments"
cd "$(dirname "$0")"

# Determine container runtime
if command -v podman &> /dev/null; then
    RUNTIME="podman"
    RUNTIME_ARGS="--userns=keep-id --user ${UID}:${GID}"
elif command -v docker &> /dev/null; then
    RUNTIME="docker"
else
    echo "Error: Neither podman, container nor docker is installed."
    exit 1
fi

case "$ACTION" in
    start)
        ADMIN_PASSWORD=$(cat ~/.secrets/n8n-experiments-passwd.txt)
        CONSOLE_PORT=$BASE_PORT
        
        # Create data and stating directories
        mkdir -p $WORK_DIR/data/vol
        mkdir -p $WORK_DIR/config/vol
        mkdir -p $WORK_DIR/logs/vol

        $RUNTIME run -d --name $CONTAINER_NAME \
            --restart unless-stopped \
            -p ${CONSOLE_PORT}:5678 $RUNTIME_ARGS \
            -v ${WORK_DIR}/data/vol:/home/node/.n8n \
            -v ${WORK_DIR}/logs/vol:/logs \
            -v ${DATA_DIR}:/data \
            -e N8N_HOST=0.0.0.0 \
            -e N8N_PORT=5678 \
            -e N8N_BASIC_AUTH_ACTIVE=true \
            -e N8N_BASIC_AUTH_USER=admin \
            -e N8N_BASIC_AUTH_PASSWORD=${ADMIN_PASSWORD} \
            -e N8N_USER_MANAGEMENT_DISABLED=true \
            -e N8N_DIAGNOSTICS_ENABLED=false \
            -e N8N_VERSION_NOTIFICATIONS_ENABLED=false \
            -e N8N_TEMPLATES_ENABLED=false \
            -e N8N_ONBOARDING_FLOW_DISABLED=true \
            -e N8N_PERSONALIZATION_ENABLED=false \
            -e N8N_SECURE_COOKIE=false \
            -e CODE_ENABLE_STDOUT=true \
            -e N8N_LOG_FILE=/logs/${CONTAINER_NAME}.log \
            -e N8N_LOG_LEVEL=debug \
            -e WEBHOOK_URL="http://${SERVER_IP}:${CONSOLE_PORT}" \
            docker.io/n8nio/n8n:latest

        $RUNTIME ps
        open "http://localhost:${CONSOLE_PORT}/"
        ;;
    stop)
        $RUNTIME stop $CONTAINER_NAME && $RUNTIME rm $CONTAINER_NAME
        ;;
    logs)
        $RUNTIME logs -f $CONTAINER_NAME
        ;;
    exec)
        shift
        $RUNTIME exec -it $CONTAINER_NAME "$@"
        ;;
    help|*)
        echo "Usage: $0 {start|stop|logs|exec|help}"
        echo "  start   - Start the n8n containers"
        echo "  stop    - Stop and remove the n8n containers"
        echo "  logs    - View the logs of the containers"
        echo "  exec    - Execute a command in the running containers"
        echo "  help    - Display this help message"
        ;;
esac