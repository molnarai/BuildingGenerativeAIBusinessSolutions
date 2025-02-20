#!/usr/bin/env python3

import argparse
import json
import logging
import os
import sys
from os.path import join as jp
import datetime
T_now = datetime.datetime.now
from typing import Dict

# from finetuning_process import (
#     validate_configuration_file,
#     validate_datafile,
#     FineTuner,
# )

DEFAULT_LOG_FILE = jp("logs", "finetuning_process.log")

def main(
        logger, 
        action: str,
        model_name: str,
        config: Dict,
        dataset_path: str,
        save_path: str,
        model_path: str,
        hub_token: str,
        max_runtime_minutes: int = 30) -> None:
         
    logger.info("Finetuning process started")
    logger.info(f"Action: {action}")
    logger.info(f"Model name: {model_name}")
    logger.info(f"Configuration: {config}")
    logger.info(f"Dataset path: {dataset_path}")
    logger.info(f"Save path: {save_path}")
    logger.info(f"Model path: {model_path}")
    logger.info(f"Hub token: {hub_token}")
    logger.info(f"Max runtime minutes: {max_runtime_minutes}")
    logger.info("Done.")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Finetuning process")
    parser.add_argument("--action", type=str, help="Action to perform")
    parser.add_argument("--model", type=str, help="Model name")
    parser.add_argument("--tag", type=str, help="Model tag, on-behalf-of username")
    parser.add_argument("--configuration-file", type=str, help="Configuration file")
    parser.add_argument("--data-dir", type=str, help="Dataset path")
    parser.add_argument("--save-dir", type=str, help="Save path")
    parser.add_argument("--model-dir", type=str, help="Model path")
    parser.add_argument("--cache-dir", type=str, help="cache path")
    parser.add_argument("--output-dir", type=str, help="output path")
    parser.add_argument("--hf-token", type=str, help="Hub token")
    parser.add_argument("--log-level", type=str, help="Log level")
    parser.add_argument("--log-dir", type=str, default=DEFAULT_LOG_FILE, help="Log file")
    parser.add_argument("--max-runtime-minutes", type=int, default=30, help="Max runtime minutes")
    args = parser.parse_args()

    os.makedirs(args.log_dir, exist_ok=True)
    os.makedirs(args.save_path, exist_ok=True)
    os.makedirs(args.model_path, exist_ok=True)
    os.makedirs(args.cache_dir, exist_ok=True)
    os.makedirs(args.output_dir, exist_ok=True)

    logfilename = jp(args.log_dir, f"finetuning_process_{args.model.replace('/', '-')}_{args.tag}.log")
    logging.basicConfig(filename=logfilename, level=args.log_level, format='%(asctime)s %(levelname)s %(name)s %(message)s')
    logger = logging.getLogger(__name__)
    logger.setLevel(args.log_level)

    logger.info("Starting finetuning process")
    logger.info(f"Arguments: {args}")
    logger.info(f"Model name: {args.model_name}")
    logger.info(f"Configuration file: {args.configuration_file}")

    config = json.load(open(args.configuration_file, "r", encoding="utf-8"))
    logger.info(f"Configuration: {config}")

    main(logger=logger,
        action=args.action,
        model_name=args.model_name,
        config=config,
        dataset_path=args.data_dir,
        save_path=args.save_path,
        model_path=args.model_path,
        hub_token=args.hf_token,
        max_runtime_minutes=args.max_runtime_minutes
    )
