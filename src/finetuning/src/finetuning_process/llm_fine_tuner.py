#!/usr/bin/env python3
TITLE = r"""
  _     _     __  __   _____ _                _____                      
 | |   | |   |  \/  | |  ___(_)_ __   ___    |_   _|   _ _ __   ___ _ __ 
 | |   | |   | |\/| | | |_  | | '_ \ / _ \_____| || | | | '_ \ / _ \ '__|
 | |___| |___| |  | | |  _| | | | | |  __/_____| || |_| | | | |  __/ |   
 |_____|_____|_|  |_| |_|   |_|_| |_|\___|     |_| \__,_|_| |_|\___|_|   
                                                                         
"""
import os
import sys
import json
import logging
import time
import argparse
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch
from trl import SFTTrainer
from transformers import TrainingArguments, TextStreamer, DataCollatorForLanguageModeling
from unsloth.chat_templates import get_chat_template
from unsloth import FastLanguageModel
from datasets import Dataset
from unsloth import is_bfloat16_supported

# Saving model
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from typing import List, Dict, Union


class LLMFineTuner:
    def __init__(self, tag: str, model_name: str, dataset: str, output_dir: str, cache_dir: str):
        self.model_name = model_name
        self.dataset = dataset
        self.output_dir = output_dir
        self.model, self.tokenizer = self.load_model_and_tokenizer()
        self.trainer = self.setup_trainer()

    def load_model_and_tokenizer(self):
        model, tokenizer = FastLanguageModel.from_pretrained(
            model_name=self.model_name,
            max_seq_length=2048,
            dtype=torch.bfloat16 if is_bfloat16_supported() else torch.float16,
            load_in_4bit=True,
        )
        tokenizer = get_chat_template(tokenizer, chat_template="unsloth", mapping={"role": "system", "content": "system"})
        return model, tokenizer

    def setup_trainer(self):
        trainer = SFTTrainer(
            model=self.model,
            tokenizer=self.tokenizer,
            train_dataset=self.dataset,
            dataset_text_field="text",
            max_seq_length=2048,
            dataset_num_proc=2,
            packing=True,
            args=TrainingArguments(
                per_device_train_batch_size=2,
                gradient_accumulation_steps=4,
                warmup_steps=5,
                max_steps=60,
                learning_rate=2e-4,
                fp16=not is_bfloat16_supported(),
                bf16=is_bfloat16_supported(),
                logging_steps=1,
                output_dir=self.output_dir,
                optim="adamw_8bit",
                seed=32,
            ),
        )
        return trainer

    def train(self):
        self.trainer.train()
        self.save_model()

    def save_model(self):
        self.model.save_pretrained(self.output_dir)
        self.tokenizer.save_pretrained(self.output_dir)


def main():
    model_name = "unsloth/Llama-3.2-1B-bnb-4bit"
    dataset = Dataset.from_json("data/processed/llm_finetuning_data.json")
    output_dir = "models/llm_finetuned_model"
    llm_fine_tuner = LLMFineTuner(model_name, dataset, output_dir)
    llm_fine_tuner.train()

    max_seq_length = 5020
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name="unsloth/Llama-3.2-1B-bnb-4bit",
        max_seq_length=max_seq_length,
        load_in_4bit=True,
        dtype=None,
        trust_remote_code=True,
    )

    model = FastLanguageModel.get_peft_model(
        model,
        r=16,
        lora_alpha=16,
        lora_dropout=0,
        target_modules=["q_proj", "k_proj", "v_proj", "up_proj", "down_proj", "o_proj", "gate_proj"],
        use_rslora=True,
        use_gradient_checkpointing="unsloth",
        random_state = 32,
        loftq_config = None,
    )
    print(model.print_trainable_parameters())