import os
jp = os.path.join
import glob
import numpy as np
import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt

import torch
from trl import SFTTrainer
from transformers import TrainingArguments, TextStreamer, DataCollatorForLanguageModeling
from unsloth.chat_templates import get_chat_template
from unsloth import FastLanguageModel
from datasets import Dataset
from unsloth import is_bfloat16_supported
import requests
import logging
import argparse
import json

# Saving model
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from typing import List, Dict, Any, Optional, Union


# Warnings
import warnings
warnings.filterwarnings("ignore")


DEFAULT_LOG_FILE = os.path.join(os.path.dirname(__file__), "finetuning_process.log")


def validate_datafile(file_path) -> Dict[str, Any]:
    """
    Validate the data file.

    Args:
        file_path (str): The path to the data file.

    Returns:
        Dict[str, Any]: The data file.
    """
    # Check if the file exists
    if not os.path.exists(file_path):
        return { "valid": False, "message": f"File {file_path} does not exist." }

    # Check if the file is a parquet file
    if not file_path.endswith(".parquet"):
        return { "valid": False, "message": f"File {file_path} is not a parquet file." }

    # Check if the file is not empty
    if os.path.getsize(file_path) == 0:
        return { "valid": False, "message": f"File {file_path} is empty." }

    # Check if the file is not corrupted
    try:
        df = pd.read_json('data/mental_health_counseling_conversations_dataset.json', lines=True)
        print(f"Number of records: {df.shape[0]:,}")
        assert set(df.columns) == {'Context', 'Response'}, f"Invalid columns: {df.columns}\n\nShould be: ['Context', 'Response']"
        assert df.shape[0]>=10, f"A minimumn of 10 records is required. You provided {df.shape[0]:,}"
        assert str(df.dtypes['Context']) == 'object', "Column 'Context' is not of type Object"
        assert str(df.dtypes['Response']) == 'object', "Column 'Context' is not of type Object"
        assert not pd.isnull(df['Context']).any(), "There are NULL values in 'Context'"
        assert not pd.isnull(df['Response']).any(), "There are NULL values in 'Response'"
    except Exception as e:
        return { "valid": False, "message": f"File {file_path} is corrupted." }

    return { "valid": True, "message": f"File {file_path} is valid." }


def validate_configuration_file(
    logger: logging.Logger,
    file_path: str
    ) -> Dict[str, Any]:
    """
    Validate the configuration file.

    Args:
        file_path (str): The path to the configuration file.

    Returns:
        Dict[str, Any]: The configuration file.
    """        
    # Check if the file exists
    if not os.path.exists(file_path):
        return { "valid": False, "message": f"File {file_path} does not exist." }

    # Check if the file is a json file
    if not file_path.endswith(".json"):
        return { "valid": False, "message": f"File {file_path} is not a json file." }

    # Check if the file is not empty
    if os.path.getsize(file_path) == 0:
        return { "valid": False, "message": f"File {file_path} is empty." }
    
    # Check if the file is not corrupted
    try:
        configuration = json.load(open(file_path, "r", encoding="utf-8"))
        assert set(configuration.keys()) == {'max_seq_length', 'learning_rate', 'epochs', 'batch_size'}, f"Invalid keys: {configuration.keys()}\n\nShould be: ['max_seq_length', 'learning_rate', 'epochs', 'batch_size']"
        assert isinstance(configuration['max_seq_length'], int), "max_seq_length is not an integer"
        assert isinstance(configuration['learning_rate'], float), "learning_rate is not a float"
        assert isinstance(configuration['epochs'], int), "epochs is not an integer"
        assert isinstance(configuration['batch_size'], int), "batch_size is not an integer"
        assert configuration['max_seq_length'] > 0, "max_seq_length is not positive"
        assert configuration['learning_rate'] > 0, "learning_rate is not positive"
        assert configuration['epochs'] > 0, "epochs is not positive"
        assert configuration['batch_size'] > 0, "batch_size is not positive"
    except Exception as e:
        return { "valid": False, "message": f"File {file_path} is corrupted." }
    
    return { "valid": True, "message": f"File {file_path} is valid." }


class FineTuner:
    def __init__(self, 
                 logger: logging.Logger,
                 model_name: str, 
                 configuration: Dict, 
                 dataset_path: str, 
                 save_path: str, 
                 model_path: str, 
                 cache_path: str,
                 hub_token: str, 
                 max_runtime_minutes: int = 60):
        self.logger = logger
        self.model_name = model_name
        self.configuration = configuration
        self.dataset_path = dataset_path
        
        self.save_path = save_path
        self.cache_path = cache_path if cache_path[-1] == '/' else f"{cache_path}/"
        self.model_path = model_path
        self.hub_token = hub_token
        self.max_runtime_minutes = max_runtime_minutes

        # future:
        self.model = None
        self.tokenizer = None
        self.dataset = None
        self.trainer = None

        # Load dataset
    def load_dataset(self):
        if not os.path.exists(self.dataset_path):
            self.logger.error(f"Dataset path {self.dataset_path} does not exist.")
            raise ValueError(f"Dataset path {self.dataset_path} does not exist.")
        
        
        # quick helper statement to add data for testing!!!
        url = "hf://datasets/Amod/mental_health_counseling_conversations/combined_dataset.json"
        df1 = pd.read_json(url, lines=True)
        print(df1.head())
        
        new_file_path = os.path.join(self.dataset_path, "mental_health_counseling_conversations_dataset.json")
        df1.to_json(new_file_path, orient="records")
                                
        df2 = pd.read_json(new_file_path, lines=True)      
        print(df2.head())
        

        datafiles = []
        if os.path.isdir(self.dataset_path):
            datafiles = glob.glob(os.path.join(self.dataset_path, "*.json"))
            if len(datafiles) == 0:
                self.logger.error(f"No data files found in {self.dataset_path}.")
                raise ValueError(f"No data files found in {self.dataset_path}.")
        else:
            datafiles = [self.dataset_path] 

        dataframes = [
            pd.read_json(datafile, lines=True) for datafile in datafiles
        ]
        df = pd.concat(dataframes)
        print(f"Dataset loaded. Number of records: {df.shape[0]:,}")
        self.logger.info(f"Dataset loaded. Number of records: {df.shape[0]:,}")
        # print(self.dataset)

        data_prompt = """Analyze the provided text from a mental health perspective. Identify any indicators of emotional distress, coping mechanisms, or psychological well-being. Highlight any potential concerns or positive aspects related to mental health, and provide a brief explanation for each observation.

        ### Input:
        {}

        ### Response:
        {}"""

        EOS_TOKEN = self.tokenizer.eos_token
        def formatting_prompt(examples):
            inputs       = examples["Context"]
            outputs      = examples["Response"]
            texts = []
            for input_, output in zip(inputs, outputs):
                text = data_prompt.format(input_, output) + EOS_TOKEN
                texts.append(text)
            return { "text" : texts, }
        
        training_data = Dataset.from_pandas(df)
        training_data = training_data.map(formatting_prompt, batched=True)
        self.dataset = training_data


        # Load model
    def load_model(self):
        self.model, self.tokenizer = FastLanguageModel.from_pretrained(
            model_name=self.model_name,
            max_seq_length=self.configuration["max_seq_length"],
            dtype=torch.bfloat16 if is_bfloat16_supported() else torch.float16,
            load_in_4bit=True,
            cache_dir=self.cache_path,
            token=self.hub_token
        )
        print("Model loaded")
        print(self.model)

        # Load trainer
    def load_trainer(self):
        self.trainer = SFTTrainer(
            model=self.model,
            tokenizer=self.tokenizer,
            train_dataset=self.dataset,
            # dataset_text_field="text",
            max_seq_length=self.configuration["max_seq_length"],
            dataset_num_proc=2,
            packing=True,
            args=TrainingArguments(
                learning_rate=3e-4,
                lr_scheduler_type="linear",
                per_device_train_batch_size=16,
                gradient_accumulation_steps=8,
                num_train_epochs=40,
                fp16=not is_bfloat16_supported(),
                bf16=is_bfloat16_supported(),
                logging_steps=1,
                optim="adamw_8bit",
                weight_decay=0.01,
                warmup_steps=10,
                output_dir="output",
                seed=0,
            ),
            cache_dir=self.cache_path,
        )
        print("Trainer loaded")
        print(self.trainer)

        # Train model
        self.trainer.train()
        print("Model trained")

        # Save model
        self.trainer.save_model(self.save_path)
        print("Model saved")

        # # Push model to hub
        # self.model.push_to_hub(
        #     self.model_path,
        #     use_temp_path=False,
        #     token=self.hub_token,
        # )
        # print("Model pushed to hub")
        # self.tokenizer.push_to_hub(
        #     self.model_path,
        #     use_temp_path=False,
        #     token=self.hub_token,
        # )
        # print("Tokenizer pushed to hub")



