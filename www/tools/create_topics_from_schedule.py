#!/usr/bin/env python
import os
jp = os.path.join
import sys
import re
import pandas as pd
import argparse

WWW_DIR = os.path.abspath(jp(os.path.dirname(__file__), ".."))

def main(filename: str, dry_run: bool = False, over_write: bool = False):
    df = pd.read_excel(filename, sheet_name="Sheet1")
    df = df.dropna(subset=['Session'])
    df = df.fillna("")
    
    # Ensure output directory exists
    output_dir = jp(WWW_DIR, "content", "topics")
    os.makedirs(output_dir, exist_ok=True)
    
    for j, row in df.iterrows():
        session = int(row['Session'])
        topic = row['Topic']
        monday = row['Monday'].strftime("%Y-%m-%d") if row['Monday'] != "" and hasattr(row['Monday'], 'strftime') else ""
        wednesday = row['Wednesday'].strftime("%Y-%m-%d") if row['Wednesday'] != "" and hasattr(row['Wednesday'], 'strftime') else ""
        dt = f"Monday {monday}, Wednesday {wednesday}"
        # Use a proper Hugo date format for the first date
        hugo_date = monday if monday else wednesday
        if not hugo_date:
            hugo_date = "2024-01-01"  # fallback date
        output_file = jp(WWW_DIR, "content", "topics", f"topic-{session:02d}.md")
        print(f"Session {session:2d} on {dt}: {topic}")
        if not over_write and os.path.exists(output_file):
            print(f"Skipping {output_file}")
            continue
        print(f"Writing to {output_file}")
        if not dry_run:
            with open(output_file, "w", encoding="utf-8") as f:
                txt = f"""---
date: {hugo_date}
classdates: '{dt}'
draft: false
title: '{topic}'
weight: {10*session}
numsession: {session}
---

(Content not yet posted. Please check back.)

"""
                f.write(txt)

    print("Done.")
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some files.")
    parser.add_argument("filename", type=str, help="The name of the file to process")
    parser.add_argument("--test", action="store_true", help="Enable dry run mode")
    parser.add_argument("--force", action="store_true", help="Force overwriting existing files")
    args = parser.parse_args()
    main(args.filename, args.test, args.force)