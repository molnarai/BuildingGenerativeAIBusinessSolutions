#!/bin/sh

cat <<'EOF'
██╗   ██╗███╗   ██╗███████╗████████╗██████╗ ██╗   ██╗ ██████╗████████╗██╗   ██╗██████╗ ███████╗██████╗
██║   ██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██║   ██║██╔════╝╚══██╔══╝██║   ██║██╔══██╗██╔════╝██╔══██╗
██║   ██║██╔██╗ ██║███████╗   ██║   ██████╔╝██║   ██║██║        ██║   ██║   ██║██████╔╝█████╗  ██║  ██║
██║   ██║██║╚██╗██║╚════██║   ██║   ██╔══██╗██║   ██║██║        ██║   ██║   ██║██╔══██╗██╔══╝  ██║  ██║
╚██████╔╝██║ ╚████║███████║   ██║   ██║  ██║╚██████╔╝╚██████╗   ██║   ╚██████╔╝██║  ██║███████╗██████╔╝
 ╚═════╝ ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝  ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═════╝

This script is for running the simple PDF extraction service using Docker Compose.
EOF

show_help() {
    cat <<'EOF'
Usage:
  ./run-simple-chunking-with-unstructed.sh [options]

Options:
  --by-title           Use by_title chunking strategy
  --basic              Use basic chunking strategy
  --max-chunk-size N   Maximum chunk size (default: 1000)
  --max-chunk-overlap N Maximum chunk overlap (default: 0)
  -h, --help           Show this help message

Examples:
  ./run-simple-chunking-with-unstructed.sh
  ./run-simple-chunking-with-unstructed.sh --by-title
  ./run-simple-chunking-with-unstructed.sh --basic
  ./run-simple-chunking-with-unstructed.sh --by-title --max-chunk-size 1200 --max-chunk-overlap 100
EOF
}

BY_TITLE=false
BASIC=false
MAX_CHUNK_SIZE=1000
MAX_CHUNK_OVERLAP=0

while [ "$#" -gt 0 ]; do
    case "$1" in
        --by-title)
            BY_TITLE=true
            shift
            ;;
        --basic)
            BASIC=true
            shift
            ;;
        --max-chunk-size)
            MAX_CHUNK_SIZE="$2"
            shift 2
            ;;
        --max-chunk-overlap)
            MAX_CHUNK_OVERLAP="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

if command -v docker >/dev/null 2>&1; then
    echo "Using Docker"
    DOCKER_CMD="docker"
elif command -v podman >/dev/null 2>&1; then
    echo "Using Podman"
    DOCKER_CMD="podman"
else
    echo "Neither Docker nor Podman is installed. Please install one of them to proceed."
    exit 1
fi

COMPOSE_CMD="${DOCKER_CMD}-compose"

PY_ARGS="--max-chunk-size ${MAX_CHUNK_SIZE} --max-chunk-overlap ${MAX_CHUNK_OVERLAP}"
if [ "${BY_TITLE}" = "true" ]; then
    PY_ARGS="${PY_ARGS} --by-title"
fi
if [ "${BASIC}" = "true" ]; then
    PY_ARGS="${PY_ARGS} --basic"
fi

cd simple-chunking-with-unstructured || exit 1
${COMPOSE_CMD} build
${COMPOSE_CMD} run --rm chunking-with-unstructured /usr/bin/python ./src/main.py ${PY_ARGS}
