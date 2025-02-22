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

from finetuning_process import (
    validate_configuration_file,
    validate_datafile,
    FineTuner,
)

LOG_DIR = "./logs"
DEFAULT_LOG_FILE = jp("logs", "finetuning_process.log")

def main(
        logger, 
        action: str,
        model_name: str,
        config: Dict,
        dataset_path: str,
        save_path: str,
        model_path: str,
        cache_path: str,
        hub_token: str,
        max_runtime_minutes: int = 30
        ) -> None:
         
    logger.info("Finetuning process started")
    logger.info(f"Action: {action}")
    logger.info(f"Model name: {model_name}")
    logger.info(f"Configuration: {config}")
    logger.info(f"Dataset path: {dataset_path}")
    logger.info(f"Save path: {save_path}")
    logger.info(f"Model path: {model_path}")
    logger.info(f"Hub token: {hub_token}")
    logger.info(f"Max runtime minutes: {max_runtime_minutes}")

    ft = FineTuner(logger, model_name, config, dataset_path, save_path, model_path, cache_path, hub_token, max_runtime_minutes)
    logger.info("FineTuner initialized")

    ft.load_model()
    
    ft.load_dataset()

    ft.load_trainer()

    logger.info("Done.")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Finetuning process")
    parser.add_argument("--action", type=str, default="info", help="Action to perform")
    parser.add_argument("--model", type=str, help="Model name")
    parser.add_argument("--tag", type=str, default="untagged", help="Model tag, on-behalf-of username")
    parser.add_argument("--configuration-file", type=str, help="Configuration file")
    parser.add_argument("--data-path", type=str, default="/staging/data", help="Dataset path")
    parser.add_argument("--save-path", type=str, default="/staging/save", help="Save path")
    parser.add_argument("--model-path", type=str, default="/staging/model", help="Model path")
    parser.add_argument("--cache-path", type=str, default="/staging/cache", help="Cache path")
    parser.add_argument("--output-path", type=str, default="/staging/output", help="Output path")
    parser.add_argument("--hf-token", type=str, default="", help="Hub token")
    parser.add_argument("--log-level", type=str, default="debug", help="Log level")
    parser.add_argument("--log-path", type=str, default=LOG_DIR, help="Log directory path")
    parser.add_argument("--log-file-path", type=str, default=DEFAULT_LOG_FILE, help="Log file")
    parser.add_argument("--max-runtime-minutes", type=int, default=30, help="Max runtime minutes")
    args = parser.parse_args()

    os.makedirs(args.log_path, exist_ok=True)
    os.makedirs(args.save_path, exist_ok=True)
    os.makedirs(args.model_path, exist_ok=True)
    os.makedirs(args.cache_path, exist_ok=True)
    os.makedirs(args.output_path, exist_ok=True)

    logfilename = jp(args.log_path, f"finetuning_process_{args.model.replace('/', '-')}_{args.tag}.log")
    logging.basicConfig(filename=logfilename, level=args.log_level, format='%(asctime)s %(levelname)s %(message)s')
    logger = logging.getLogger(__name__)
    logger.setLevel(args.log_level)

    logger.info("Starting finetuning process")
    logger.info(f"Arguments: {args}")
    logger.info(f"Model name: {args.model}")
    logger.info(f"Configuration file: {args.configuration_file}")

    res = validate_configuration_file(args.configuration_file)
    if not res["valid"]:
        logger.error(f"Configuration file is not valid: {res['message']}")
        # sys.exit(1)

    config = json.load(open(args.configuration_file, "r", encoding="utf-8"))
    logger.info(f"Configuration: {config}")

    main(
        logger=logger,
        action=args.action,
        model_name=args.model,
        config=config,
        dataset_path=args.data_path,
        save_path=args.save_path,
        model_path=args.model_path,
        cache_path=args.cache_path,
        output_path=args.output_path,
        hub_token=args.hf_token,
        max_runtime_minutes=args.max_runtime_minutes
    )
