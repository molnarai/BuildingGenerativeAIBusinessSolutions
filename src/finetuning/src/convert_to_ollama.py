import json
import os
import shutil

def create_ollama_modelfile(model_name, base_model):
    with open("Modelfile", "w") as f:
        # Write base model
        f.write(f"FROM {base_model}\n\n")
        
        # Write parameters
        f.write("PARAMETER temperature 0.7\n")
        f.write("PARAMETER top_p 0.7\n")
        f.write('PARAMETER stop "### Instruction:"\n')
        f.write('PARAMETER stop "### Response:"\n\n')
        
        # Write template
        f.write('TEMPLATE """')
        f.write("### Instruction: {{.Input}}\n\n")
        f.write("### Response: ")
        f.write('"""')

def prepare_ollama_model(model_name, source_dir):
    try:
        # Create directory for Ollama model
        os.makedirs(model_name, exist_ok=True)
        
        # Create Modelfile in the model directory
        create_ollama_modelfile(model_name, "llama2")
        
        # Copy model files
        target_dir = os.path.join(model_name, "pytorch_model")
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        shutil.copytree(source_dir, target_dir)
        
        # Copy Modelfile to the correct location
        shutil.move("Modelfile", os.path.join(model_name, "Modelfile"))
        
        print(f"Model prepared for Ollama in directory: {model_name}")
        print(f"Files copied from {source_dir} to {target_dir}")
        print("Modelfile created successfully")
        
    except Exception as e:
        print(f"Error preparing model: {str(e)}")
        raise

def verify_model_structure(model_name):
    """Verify the model directory structure is correct"""
    required_files = ["Modelfile", "pytorch_model"]
    model_path = os.path.join(os.getcwd(), model_name)
    
    for file in required_files:
        path = os.path.join(model_path, file)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Required file/directory not found: {path}")
    
    print("Model structure verification completed successfully")

if __name__ == "__main__":
    model_name = "my-finetuned-llama"
    source_dir = "./final_model"
    
    # Ensure source directory exists
    if not os.path.exists(source_dir):
        raise FileNotFoundError(f"Source directory not found: {source_dir}")
    
    # Prepare the model
    prepare_ollama_model(model_name, source_dir)
    
    # Verify the structure
    verify_model_structure(model_name)


# FROM llama2

# PARAMETER temperature 0.7
# PARAMETER top_p 0.7
# PARAMETER stop "### Instruction:"
# PARAMETER stop "### Response:"

# TEMPLATE """### Instruction: {{.Input}}

# ### Response: """