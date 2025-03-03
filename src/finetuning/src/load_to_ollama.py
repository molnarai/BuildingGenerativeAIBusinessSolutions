import subprocess
import os

def load_model_to_ollama(model_dir):
    try:
        # Create model in Ollama
        subprocess.run(["ollama", "create", model_dir, "-f", os.path.join(model_dir, "Modelfile")], check=True)
        print(f"Successfully loaded model {model_dir} into Ollama")
    except subprocess.CalledProcessError as e:
        print(f"Error loading model into Ollama: {e}")

if __name__ == "__main__":
    model_name = "my-finetuned-llama"
    load_model_to_ollama(model_name)
