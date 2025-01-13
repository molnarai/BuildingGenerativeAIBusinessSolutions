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
    for j, row in df.iterrows():
        session = int(row['Session'])
        topic = row['Topic']
        day = row['Day']
        dt = day.strftime("%Y-%m-%d")
        output_file = jp(WWW_DIR, "content", "topics", f"topic-{session:02d}.md")
        print(f"Session {session:2d} on {dt}: {topic}")
        if not over_write and os.path.exists(output_file):
            print(f"Skipping {output_file}")
            continue
        print(f"Writing to {output_file}")
        if not dry_run:
            with open(output_file, "w") as f:
                txt = f"""+++
date = '{dt}'
draft = false
title = '{topic}'
weight = {10*session}
numsession = {session}
+++

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