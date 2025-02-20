#!/bin/bash
CONTAINER_NAME="${USER}/ft_hf_unsloth"
HF_TOKEN=`cat ${HOME}/.secrets/huggingface-msa8700b.txt
CONFIG_FILE="./test_config.json"

cat<<EOF > $CONFIG_FILE
{
  "model": "unsloth/Llama-3.2-1B-bnb-4bit",
  "tag": "testing_${USER}",
  "cache_dir": "/staging/cache",
  "model_dir": "/staging/model",
  "data_dir": "/staging/data",
  "output_dir": "/staging/output",
  "log_dir": "/staging/log",
  "log_level": "DEBUG",
  "hf_token": "${HF_TOKEN}",
  "max_runtime_minutes": 30
}
EOF

# cat<<'EOT'
#   ____        _ _     _ 
#  | __ ) _   _(_) | __| |
#  |  _ \| | | | | |/ _` |
#  | |_) | |_| | | | (_| |
#  |____/ \__,_|_|_|\__,_|
                        
# EOT

podman build -t $CONTAINER_NAME -f ../Dockerfile.huggingface .

# cat<<'EOT'
#   ____                _____         _   
#  |  _ \ _   _ _ __   |_   _|__  ___| |_ 
#  | |_) | | | | '_ \    | |/ _ \/ __| __|
#  |  _ <| |_| | | | |   | |  __/\__ \ |_ 
#  |_| \_\\__,_|_| |_|   |_|\___||___/\__|
                                        
# EOT

mkdir -p /staging/users/$USER/msa8700/finetuning
podman run -it --rm \
--device nvidia.com/gpu=all \
--security-opt=label=disable \
-v $(dirname $PWD):/myapp/local \
-v /staging/users/$USER/msa8700/finetuning:/staging \
-w /myapp \
    $CONTAINER_NAME /bin/bash python3 -m local.src.finetuning_process \
    --config-file=$CONFIG_FILE \
    --action="test" \
    --model="unsloth/Llama-3.2-1B-bnb-4bit" \
    --tag="testing_${USER}" \
    --cache-dir=/staging/cache \
    --model-dir=/staging/model \
    --data-dir=/staging/data \
    --output-dir=/staging/output \
    --log-dir=/staging/log \
    --log-level=DEBUG \
    --hf-token=$HF_TOKEN \
    --max-runtime-minutes=30

 echo "Done."