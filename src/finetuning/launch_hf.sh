#!/bin/bash
CONTAINER_NAME="${USER}/ft_hf_unsloth"

case $1 in
build)
	podman build -t $CONTAINER_NAME -f Dockerfile.huggingface .
	;;

run)
        shift
        podman run -it --rm \
        --device nvidia.com/gpu=all \
        --security-opt=label=disable \
        -v $PWD:/myapp/local \
        -v /staging/users/$USER:/staging \
         $CONTAINER_NAME $*
        ;;
esac

