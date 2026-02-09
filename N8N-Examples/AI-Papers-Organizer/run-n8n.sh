#!/bin/bash
# filepath: /Users/pmolnar/Classes-Workshops/MSA8700_Building_Generative_AI_Business_Solutions/BuildingGenerativeAIBusinessSolutions/N8N-Examples/AI-Papers-Organizer/run-n8n.sh

slug() {
    echo "$1" | tr '[:upper:]' '[:lower:]' | tr -c 'a-z0-9' '-' | tr -s '-'
}

set -e

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load .env file if exists
if [ -f "$SCRIPT_DIR/.env" ]; then
    echo "Loading environment variables from .env file..."
    export $(grep -v '^#' "$SCRIPT_DIR/.env" | xargs)
fi

# Detect container runtime
if command -v docker &> /dev/null; then
    CONTAINER_CMD="docker"
    echo "Using Docker..."
elif command -v podman &> /dev/null; then
    CONTAINER_CMD="podman"
    echo "Using Podman..."
else
    echo "Error: Neither Docker nor Podman is installed."
    exit 1
fi

# Set default workflow if not defined
WORK_FLOW=${WORK_FLOW:-"AI-Papers-Organizer-with-Loop.json"}
WORKFLOW_PATH="$SCRIPT_DIR/$WORK_FLOW"
echo "Workflow file set to: $WORK_FLOW"
WORKFLOW_SLUG=$(slug $(basename -s .json $WORK_FLOW))

# Check if workflow file exists
if [ ! -f "$WORKFLOW_PATH" ]; then
    echo "Error: Workflow file $WORK_FLOW not found at $WORKFLOW_PATH"
    exit 1
fi

# Cleanup function
cleanup() {
    echo "Stopping n8n container..."
    $CONTAINER_CMD stop "n8n-$WORKFLOW_SLUG" 2>/dev/null || true
}
trap cleanup EXIT

# Run n8n container in background
echo "Starting n8n..."
$CONTAINER_CMD run -d --rm \
    --name "n8n-$WORKFLOW_SLUG" \
    -p 5678:5678 \
    -e N8N_HOST=localhost \
    -e N8N_PORT=5678 \
    -e N8N_PROTOCOL=http \
    -e GENERIC_TIMEZONE=America/New_York \
    ${OLLAMA_BASE_URL:+-e OLLAMA_BASE_URL=$OLLAMA_BASE_URL} \
    ${OLLAMA_API_KEY:+-e OLLAMA_API_KEY=$OLLAMA_API_KEY} \
    -v "$SCRIPT_DIR:/data/workflows" \
    -v n8n_data:/home/node/.n8n \
    docker.n8n.io/n8nio/n8n

echo "Waiting for n8n to be ready..."
sleep 10

# Create Ollama credentials if environment variables are set
if [ -n "$OLLAMA_BASE_URL" ] && [ -n "$OLLAMA_API_KEY" ]; then
    echo "Creating Ollama credentials..."
    $CONTAINER_CMD exec "n8n-$WORKFLOW_SLUG" sh -c "cat > /tmp/ollama-credentials.json << EOF
{
  \"name\": \"Ollama API\",
  \"type\": \"ollamaApi\",
  \"data\": {
    \"baseUrl\": \"$OLLAMA_BASE_URL\",
    \"apiKey\": \"$OLLAMA_API_KEY\"
  }
}
EOF"

    $CONTAINER_CMD exec "n8n-$WORKFLOW_SLUG" n8n import:credentials --input=/tmp/ollama-credentials.json || echo "Warning: Could not import Ollama credentials"
fi

# Import and execute workflow
echo "Importing workflow: $WORK_FLOW"
WORKFLOW_ID=$($CONTAINER_CMD exec "n8n-$WORKFLOW_SLUG" n8n import:workflow --input="/data/workflows/$WORK_FLOW" | grep -oP 'id: \K[a-zA-Z0-9]+' || echo "")

if [ -z "$WORKFLOW_ID" ]; then
    echo "Failed to import workflow. Trying to find existing workflow..."
    # If import fails, try to find existing workflow by name
    sleep 2
fi

echo "Executing workflow..."
$CONTAINER_CMD exec "n8n-$WORKFLOW_SLUG" n8n execute --id="$WORKFLOW_ID" || \
$CONTAINER_CMD exec "n8n-$WORKFLOW_SLUG" n8n execute --file="/data/workflows/$WORK_FLOW"

echo ""
echo "n8n is running at http://localhost:5678"
echo "Workflow files are mounted from: $SCRIPT_DIR"
echo "Press Ctrl+C to stop n8n"

# Follow logs
$CONTAINER_CMD logs -f "n8n-$WORKFLOW_SLUG"