import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import Dataset
import os
from trl import SFTTrainer

def prepare_model():
    model_name = "meta-llama/Llama-2-7b"  # Replace with your Llama 3.2 model name
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        token=os.environ.get("HF_TOKEN"),
        trust_remote_code=True
    )
    tokenizer.pad_token = tokenizer.eos_token

    # Load model in 4-bit precision
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        token=os.environ.get("HF_TOKEN"),
        load_in_4bit=True,
        torch_dtype=torch.bfloat16,
        device_map="auto",
    )

    # Prepare model for k-bit training
    model = prepare_model_for_kbit_training(model)

    # LoRA configuration
    lora_config = LoraConfig(
        r=16,  # Rank
        lora_alpha=32,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )

    # Create PEFT model
    model = get_peft_model(model, lora_config)
    
    return model, tokenizer

def prepare_dataset(data_path):
    # Load your dataset here
    # This is an example format - adjust according to your data
    dataset = Dataset.from_json(data_path)
    
    def format_instruction(example):
        return {
            "text": f"### Instruction: {example['instruction']}\n\n### Response: {example['response']}"
        }
    
    dataset = dataset.map(format_instruction)
    return dataset

def train_model(model, tokenizer, dataset):
    training_args = TrainingArguments(
        output_dir="./output",
        num_train_epochs=3,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        fp16=True,
        logging_steps=10,
        save_strategy="epoch",
        warmup_steps=100,
    )

    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        tokenizer=tokenizer,
        args=training_args,
        max_seq_length=2048,
    )

    trainer.train()
    return trainer

def save_model(trainer, output_dir):
    # Save the final model
    trainer.save_model(output_dir)
    
if __name__ == "__main__":
    # Set your HuggingFace token in environment variable
    assert "HF_TOKEN" in os.environ, "Please set HF_TOKEN environment variable"
    
    # Initialize model and tokenizer
    model, tokenizer = prepare_model()
    
    # Prepare dataset
    dataset = prepare_dataset("path_to_your_dataset.json")
    
    # Train model
    trainer = train_model(model, tokenizer, dataset)
    
    # Save model
    save_model(trainer, "./final_model")
