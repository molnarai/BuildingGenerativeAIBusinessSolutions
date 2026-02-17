#!/bin/bash
cat<<'EOF'
████████╗███████╗██╗  ██╗████████╗                                                                                              
╚══██╔══╝██╔════╝╚██╗██╔╝╚══██╔══╝                                                                                              
   ██║   █████╗   ╚███╔╝    ██║                                                                                                 
   ██║   ██╔══╝   ██╔██╗    ██║                                                                                                 
   ██║   ███████╗██╔╝ ██╗   ██║                                                                                                 
   ╚═╝   ╚══════╝╚═╝  ╚═╝   ╚═╝                                                                                                 
                                                                                                                                
██╗   ██╗███████╗ ██████╗████████╗ ██████╗ ██████╗     ███████╗███╗   ███╗██████╗ ███████╗██████╗ ██████╗ ██╗███╗   ██╗ ██████╗ 
██║   ██║██╔════╝██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗    ██╔════╝████╗ ████║██╔══██╗██╔════╝██╔══██╗██╔══██╗██║████╗  ██║██╔════╝ 
██║   ██║█████╗  ██║        ██║   ██║   ██║██████╔╝    █████╗  ██╔████╔██║██████╔╝█████╗  ██║  ██║██║  ██║██║██╔██╗ ██║██║  ███╗
╚██╗ ██╔╝██╔══╝  ██║        ██║   ██║   ██║██╔══██╗    ██╔══╝  ██║╚██╔╝██║██╔══██╗██╔══╝  ██║  ██║██║  ██║██║██║╚██╗██║██║   ██║
 ╚████╔╝ ███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║    ███████╗██║ ╚═╝ ██║██████╔╝███████╗██████╔╝██████╔╝██║██║ ╚████║╚██████╔╝
  ╚═══╝  ╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝    ╚══════╝╚═╝     ╚═╝╚═════╝ ╚══════╝╚═════╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝ 
                                                                                                                                
EOF
### docker or podman
if command -v docker &> /dev/null
then
    echo "Using Docker"
    DOCKER_CMD="docker compose"
elif command -v podman &> /dev/null
then
    echo "Using Podman"
    DOCKER_CMD="podman-compose"
else
    echo "Neither Docker nor Podman is installed. Please install one of them to proceed."
    exit 1
fi
pushd text-to-vector-embedding-with-huggingface
${DOCKER_CMD} build
${DOCKER_CMD} up -d
# wait until all services are up
until ${DOCKER_CMD} exec vector-embedder echo "Vector Embedder is up"
do
    sleep 3
done
${DOCKER_CMD} exec vector-embedder ./run.sh
# Ask user if they want to shutdown. Need to respond with 'yes'
read -p "Do you want to shutdown the services? (yes/no) " answer
if [[ "$answer" == "yes" ]]; then
    ${DOCKER_CMD} down
else
    echo "Services are still running. You can shutdown later with '${DOCKER_CMD} down'"
fi
popd