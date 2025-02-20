#!/bin/bash
CONTAINER_NAME="${USER}/ft_hf_unsloth"
ROOT_DIR=$(dirname $0)

case $1 in
build)
	podman build -t $CONTAINER_NAME -f Dockerfile.huggingface .
	;;

shell)
        shift
        podman run -it --rm \
        --device nvidia.com/gpu=all \
        --security-opt=label=disable \
        -v $PWD:/myapp/local \
        -v /staging/users/$USER:/staging \
         $CONTAINER_NAME $*
        ;;

finetun*)
        mkdir -p /staging/users/$USER/msa8700/finetuning
        podman run -it --rm \
                --device nvidia.com/gpu=all \
                --security-opt=label=disable \
                -v ${ROOT_DIR}:/myapp/local \
                -v /staging/users/$USER/msa8700/finetuning:/staging \
                $CONTAINER_NAME /usr/bin/python3 -m finetuning_process \
                --action="test" \
                --model="unsloth/Llama-3.2-1B-bnb-4bit" \
                --tag="testing_${USER}" \
                --configuration-file=/myapp/local/config.json \
                --cache-dir=/staging/cache \
                --model-dir=/staging/model \
                --data-dir=/staging/data \
                --output-dir=/staging/output \
                --log-dir=/staging/log \
                --log-level=DEBUG \
                --hf-token=$HF_TOKEN \
                --max-runtime-minutes=30
        ;;

esac

