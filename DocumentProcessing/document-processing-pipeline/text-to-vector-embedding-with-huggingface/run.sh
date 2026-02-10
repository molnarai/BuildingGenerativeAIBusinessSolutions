#!/bin/bash

# Text to Vector Embedding Pipeline Runner
# Usage: ./run.sh [command] [options]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="${SCRIPT_DIR}/src"
DATA_DIR="${SCRIPT_DIR}/data"
INPUT_DIR="${DATA_DIR}/input"

# Functions
print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Check if Python is installed
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed"
        exit 1
    fi
    print_success "Python 3 found: $(python3 --version)"
}

# Setup virtual environment
setup_venv() {
    print_header "Setting up Virtual Environment"
    
    if [ ! -d "${SCRIPT_DIR}/venv" ]; then
        print_info "Creating virtual environment..."
        python3 -m venv "${SCRIPT_DIR}/venv"
        print_success "Virtual environment created"
    else
        print_info "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    source "${SCRIPT_DIR}/venv/bin/activate"
    print_success "Virtual environment activated"
    
    # Install requirements
    print_info "Installing dependencies..."
    pip install -q --upgrade pip
    pip install -q -r "${SCRIPT_DIR}/requirements.txt"
    print_success "Dependencies installed"
}

# Run the simple example
run_example() {
    print_header "Running Vector Embedding Example"
    check_python
    cd "$SRC_DIR"
    python3 vector_embedding.py
}

# Run the main pipeline
run_pipeline() {
    print_header "Running Main Pipeline"
    check_python
    
    # Create input directory if it doesn't exist
    mkdir -p "$INPUT_DIR"
    
    # Check if there are any .txt files
    if [ -z "$(ls -A ${INPUT_DIR}/*.txt 2>/dev/null)" ]; then
        print_error "No .txt files found in ${INPUT_DIR}"
        print_info "Please add text files to process"
        exit 1
    fi
    
    cd "$SRC_DIR"
    python3 main.py "$@"
}

# Run with custom parameters
run_custom() {
    print_header "Running Pipeline with Custom Parameters"
    check_python
    cd "$SRC_DIR"
    python3 main.py \
        --input-dir "${INPUT_DIR}" \
        --chunk-size 300 \
        --chunk-overlap 75 \
        --model-name "all-MiniLM-L6-v2" \
        --batch-size 32 \
        --opensearch-host localhost \
        --opensearch-port 9200 \
        --index-name custom-embeddings \
        "$@"
}

# Check OpenSearch connection
check_opensearch() {
    print_header "Checking OpenSearch Connection"
    
    local host=${1:-localhost}
    local port=${2:-9200}
    
    print_info "Checking ${host}:${port}..."
    
    if curl -s "http://${host}:${port}" > /dev/null; then
        print_success "OpenSearch is running"
        curl -s "http://${host}:${port}" | python3 -m json.tool
    else
        print_error "Cannot connect to OpenSearch at ${host}:${port}"
        print_info "Start OpenSearch with: docker run -p 9200:9200 -e \"discovery.type=single-node\" opensearchproject/opensearch:latest"
        exit 1
    fi
}

# Start OpenSearch with Docker
start_opensearch() {
    print_header "Starting OpenSearch with Docker"
    
    if docker ps | grep -q opensearch; then
        print_info "OpenSearch is already running"
    else
        print_info "Starting OpenSearch container..."
        docker run -d \
            --name opensearch \
            -p 9200:9200 \
            -p 9600:9600 \
            -e "discovery.type=single-node" \
            -e "OPENSEARCH_INITIAL_ADMIN_PASSWORD=Admin123!" \
            opensearchproject/opensearch:latest
        
        print_success "OpenSearch started"
        print_info "Waiting for OpenSearch to be ready..."
        sleep 10
        check_opensearch
    fi
}

# Stop OpenSearch
stop_opensearch() {
    print_header "Stopping OpenSearch"
    
    if docker ps | grep -q opensearch; then
        docker stop opensearch
        docker rm opensearch
        print_success "OpenSearch stopped and removed"
    else
        print_info "OpenSearch is not running"
    fi
}

# Create sample data
create_sample_data() {
    print_header "Creating Sample Data"
    
    mkdir -p "$INPUT_DIR"
    
    # Sample document 1
    cat > "${INPUT_DIR}/sample1.txt" << 'EOF'
OpenSearch is a community-driven, open source search and analytics suite derived from Apache 2.0 licensed Elasticsearch 7.10.2 & Kibana 7.10.2. It consists of a search engine daemon, OpenSearch, and a visualization and user interface, OpenSearch Dashboards.

OpenSearch enables people to easily ingest, secure, search, aggregate, view, and analyze data. These capabilities are popular for use cases such as application search, log analytics, and more. With OpenSearch people benefit from having an open source product they can use, modify, extend, monetize, and resell how they want.
EOF

    # Sample document 2
    cat > "${INPUT_DIR}/sample2.txt" << 'EOF'
Vector search is a technique that allows you to find similar items based on their vector representations. In OpenSearch, vector search is implemented using the k-NN (k-nearest neighbors) plugin, which provides efficient approximate nearest neighbor search capabilities.

The k-NN plugin uses algorithms like HNSW (Hierarchical Navigable Small World) to enable fast similarity search over large datasets. This is particularly useful for semantic search, recommendation systems, and anomaly detection.
EOF

    # Sample document 3
    cat > "${INPUT_DIR}/sample3.txt" << 'EOF'
Machine learning embeddings transform text, images, or other data into dense vector representations. These embeddings capture semantic meaning, allowing similar items to be close together in vector space.

Popular embedding models include BERT, Sentence-BERT, and GPT-based models. These models are pre-trained on large datasets and can be fine-tuned for specific tasks. The embedding dimension typically ranges from 384 to 1536 dimensions.
EOF

    print_success "Created 3 sample files in ${INPUT_DIR}"
    ls -lh "${INPUT_DIR}"/*.txt
}

# Clean data
clean_data() {
    print_header "Cleaning Data"
    
    if [ -d "$INPUT_DIR" ]; then
        rm -f "${INPUT_DIR}"/*.txt
        print_success "Removed all .txt files from ${INPUT_DIR}"
    fi
}

# Show help
show_help() {
    cat << EOF
${BLUE}Text to Vector Embedding Pipeline${NC}

${GREEN}Usage:${NC}
    ./run.sh [command] [options]

${GREEN}Commands:${NC}
    ${YELLOW}setup${NC}              Setup virtual environment and install dependencies
    ${YELLOW}example${NC}            Run the simple vector embedding example
    ${YELLOW}pipeline${NC}           Run the main pipeline (processes all .txt files)
    ${YELLOW}custom${NC}             Run with custom parameters
    ${YELLOW}check-opensearch${NC}   Check OpenSearch connection
    ${YELLOW}start-opensearch${NC}   Start OpenSearch with Docker
    ${YELLOW}stop-opensearch${NC}    Stop OpenSearch Docker container
    ${YELLOW}sample-data${NC}        Create sample .txt files in data/input
    ${YELLOW}clean${NC}              Remove all .txt files from data/input
    ${YELLOW}help${NC}               Show this help message

${GREEN}Examples:${NC}
    # Setup environment
    ./run.sh setup

    # Run simple example
    ./run.sh example

    # Create sample data and run pipeline
    ./run.sh sample-data
    ./run.sh start-opensearch
    ./run.sh pipeline

    # Run with custom options
    ./run.sh pipeline --chunk-size 500 --model-name "all-mpnet-base-v2"

    # Check OpenSearch status
    ./run.sh check-opensearch

${GREEN}Notes:${NC}
    - Place your .txt files in data/input/ directory
    - OpenSearch must be running before running the pipeline
    - Use --help with pipeline command for more options

EOF
}

# Main script logic
case "${1:-help}" in
    setup)
        check_python
        setup_venv
        ;;
    example)
        run_example
        ;;
    pipeline)
        shift
        run_pipeline "$@"
        ;;
    custom)
        shift
        run_custom "$@"
        ;;
    check-opensearch)
        check_opensearch "${2:-localhost}" "${3:-9200}"
        ;;
    start-opensearch)
        start_opensearch
        ;;
    stop-opensearch)
        stop_opensearch
        ;;
    sample-data)
        create_sample_data
        ;;
    clean)
        clean_data
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
