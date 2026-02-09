#!/bin/bash
cat<<'EOF'
███████╗██╗███╗   ███╗██████╗ ██╗     ███████╗    ██████╗ ██████╗ ███████╗      
██╔════╝██║████╗ ████║██╔══██╗██║     ██╔════╝    ██╔══██╗██╔══██╗██╔════╝      
███████╗██║██╔████╔██║██████╔╝██║     █████╗      ██████╔╝██║  ██║█████╗        
╚════██║██║██║╚██╔╝██║██╔═══╝ ██║     ██╔══╝      ██╔═══╝ ██║  ██║██╔══╝        
███████║██║██║ ╚═╝ ██║██║     ███████╗███████╗    ██║     ██████╔╝██║           
╚══════╝╚═╝╚═╝     ╚═╝╚═╝     ╚══════╝╚══════╝    ╚═╝     ╚═════╝ ╚═╝           
                                                                                
███████╗██╗  ██╗████████╗██████╗  █████╗  ██████╗████████╗██╗ ██████╗ ███╗   ██╗
██╔════╝╚██╗██╔╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║
█████╗   ╚███╔╝    ██║   ██████╔╝███████║██║        ██║   ██║██║   ██║██╔██╗ ██║
██╔══╝   ██╔██╗    ██║   ██╔══██╗██╔══██║██║        ██║   ██║██║   ██║██║╚██╗██║
███████╗██╔╝ ██╗   ██║   ██║  ██║██║  ██║╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║
╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
                                                                                
This script is for running the simple PDF extraction service using Docker Compose.
EOF
### docker or podman
if command -v docker &> /dev/null
then
    echo "Using Docker"
    DOCKER_CMD="docker"
elif command -v podman &> /dev/null
then
    echo "Using Podman"
    DOCKER_CMD="podman"
else
    echo "Neither Docker nor Podman is installed. Please install one of them to proceed."
    exit 1
fi
pushd simple-pdf-extraction
${DOCKER_CMD}-compose build
${DOCKER_CMD}-compose run --rm pdf-extractor ./run.sh
popd