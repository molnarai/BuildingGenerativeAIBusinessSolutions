import os
jp = os.path.join
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


def validate_configuration_file(file_path) -> Dict[str, Any]:
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
    def __init__(self, logger: logging.Logger,
                 model_name: str, configuration_file: str, dataset_path: str, save_path: str, model_path: str,
                 hub_token: str, max_runtime_minutes: int = 60):
        self.model_name = model_name
        self.configuration_file = configuration_file
        self.dataset_path = dataset_path
        self.save_path = save_path
        self.model_path = model_path
        self.hub_token = hub_token
        self.max_runtime_minutes = max_runtime_minutes

        # Load configuration
    def load_configuration(self):
        self.configuration = json.load(open(self.configuration_file, "r", encoding="utf-8"))
        print("Configuration loaded")
        print(self.configuration)

        # Load dataset
    def load_dataset(self):
        self.dataset = Dataset.from_parquet(self.dataset_path)
        print("Dataset loaded")
        print(self.dataset)

        # Load model
    def load_model(self):
        self.model, self.tokenizer = FastLanguageModel.from_pretrained(
            model_name=self.model_name,
            max_seq_length=self.configuration["max_seq_length"],
            dtype=torch.bfloat16 if is_bfloat16_supported() else torch.float16,
            load_in_4bit=True,
        )
        print("Model loaded")
        print(self.model)

        # Load trainer
    def load_trainer(self):
        self.trainer = SFTTrainer(
            model=self.model,
            tokenizer=self.tokenizer,
            train_dataset=self.dataset,
            dataset_text_field="text",
            max_seq_length=self.configuration["max_seq_length"],
            dataset_num_proc=2,
        )
        print("Trainer loaded")
        print(self.trainer)

        # Train model
        self.trainer.train()
        print("Model trained")

        # Save model
        self.trainer.save_model(self.save_path)
        print("Model saved")

        # Push model to hub
        self.model.push_to_hub(
            self.model_path,
            use_temp_dir=False,
            token=self.hub_token,
        )
        print("Model pushed to hub")
        self.tokenizer.push_to_hub(
            self.model_path,
            use_temp_dir=False,
            token=self.hub_token,
        )
        print("Tokenizer pushed to hub")



def main(logger, model_name: str, configuration_file: str, dataset_path: str, save_path: str, model_path: str, 
        hub_token: str, max_runtime_minutes: int = 60) -> None:
    # Load configuration
    configuration = json.load(open(configuration_file, "r", encoding="utf-8"))
    print("Configuration loaded")
    print(configuration)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Finetuning process")
    parser.add_argument("--action", type=str, help="Action to perform")
    parser.add_argument("--model", type=str, help="Model name")
    parser.add_argument("--tag", type=str, help="Model tag, on-behalf-of username")
    parser.add_argument("--configuration-file", type=str, help="Configuration file")
    parser.add_argument("--data-dir", type=str, help="Dataset path")
    parser.add_argument("--save-dir", type=str, help="Save path")
    parser.add_argument("--model-dir", type=str, help="Model path")
    parser.add_argument("--hf-token", type=str, help="Hub token")
    parser.add_argument("--max-runtime-minutes", type=int, help="Max runtime minutes")
    parser.add_argument("--log-level", type=str, help="Log level")
    parser.add_argument("--log-dir", type=str, default=DEFAULT_LOG_FILE, help="Log file")
    args = parser.parse_args()

    os.makedirs(args.log_dir, exist_ok=True)
    os.makedirs(args.save_path, exist_ok=True)
    os.makedirs(args.model_path, exist_ok=True)
    os.makedirs(args.cache_dir, exist_ok=True)
    logfilename = jp(args.log_dir, f"finetuning_process_{args.model.replace('/', '-')}_{args.tag}.log")
    logging.basicConfig(filename=logfilename, level=args.log_level, format='%(asctime)s %(levelname)s %(name)s %(message)s')
    logger = logging.getLogger(__name__)
    logger.info("Starting finetuning process")
    logger.info(f"Arguments: {args}")
    logger.info(f"Model name: {args.model_name}")
    logger.info(f"Configuration file: {args.configuration_file}")
    ## main()
