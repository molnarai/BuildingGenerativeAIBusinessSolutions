import subprocess
subprocess.Popen(["ollama", "serve"])
import time
time.sleep(5) # Wait for a few seconds for Ollama to load!

# Perform inference with original model before finetuning:
unsloth_model = "unsloth/Llama-3.2-1B-bnb-4bit"

command = "curl http://localhost:11434/api/chat -d \
    {'model_name': 'unsloth/Llama-3.2-1B-bnb-4bit', \
    'messages': ['text': 'I\'m going through some things with my feelings and myself. \
        I barely sleep and I do nothing but think about how I'm worthless \
            and how I shouldn't be here. I've never tried or contemplated suicide. \
                I've always wanted to fix my issues, but I never get around to it. \
                    How can I change my feeling of being worthless to everyone?']}"
process = subprocess.run(command, shell=True, capture_output=True, text=True)

command = "ollama run 'unsloth/Llama-3.2-1B-bnb-4bit'"
process = subprocess.run(command, shell=True, capture_output=True, text=True)

# Perform inference with finetuned model:
command = "ollama create unsloth_finetuned_model -f ./model/Modelfile"
process = subprocess.run(command, shell=True, capture_output=True, text=True)

command = "curl http://localhost:11434/api/chat -d \
    {'model_name': 'unsloth_finetuned_model', \
    'messages': ['text': 'I\'m going through some things with my feelings and myself. \
        I barely sleep and I do nothing but think about how I'm worthless \
            and how I shouldn't be here. I've never tried or contemplated suicide. \
                I've always wanted to fix my issues, but I never get around to it. \
                    How can I change my feeling of being worthless to everyone?']}"
process = subprocess.run(command, shell=True, capture_output=True, text=True)

command = "ollama run unsloth_finetuned_model"
process = subprocess.run(command, shell=True, capture_output=True, text=True)
