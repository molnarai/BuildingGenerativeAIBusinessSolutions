#!/bin/bash
CONTAINER_NAME="${USER}/ftunsloth"

case $1 in
build)
	podman build -t $CONTAINER_NAME -f Dockerfile .
	;;

jupyter)
	PORT=${2:-19034}
	podman run --rm \
	-p ${PORT}:8888 \
	--device nvidia.com/gpu=0 \
	--security-opt=label=disable \
	-v $PWD:/myapp/local \
	 $CONTAINER_NAME jupyter-lab
	;;
run)
        podman run -it --rm \
        --device nvidia.com/gpu=all \
        --security-opt=label=disable \
        -v $PWD:/myapp/local \
         $CONTAINER_NAME $2 $3 $4 
        ;;
esac

