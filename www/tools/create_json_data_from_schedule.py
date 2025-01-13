#!/usr/bin/env python
import os
jp = os.path.join
import sys
import re
import pandas as pd
import argparse
import json
import datetime

WWW_DIR = os.path.abspath(jp(os.path.dirname(__file__), ".."))

def main(filename: str, dry_run: bool = False, over_write: bool = False):
    df = pd.read_excel(filename, sheet_name="Sheet1")
    df['Session'] = df['Session'].map(lambda x: str(int(x)), na_action="ignore")
    markdown = df.rename(lambda s: s.replace(' ', ''), axis=1).to_markdown(index=False)
    html = df.to_html(index=False, classes="table table-striped table-hover")
    df.fillna("", inplace=True)
    df["Day"] = df["Day"].map(lambda x: x.strftime("%Y-%m-%d"))
    data = df.to_dict(orient='records')
    
    markdown = df.to_markdown(index=False)

    output_file = jp(WWW_DIR, "data", "schedule.json")
    html_file = jp(WWW_DIR, "content", "schedule.html")
    markdown_file = jp(WWW_DIR, "content", "schedule.md")

    if not dry_run:
        if not over_write and os.path.exists(markdown_file):
            print(f"Skipping {markdown_file}")
        else:
            print(f"Writing to {markdown_file}")
            with open(markdown_file, "w") as f:
                f.write(markdown)
                f.write("\n")

        if not over_write and os.path.exists(html_file):
            print(f"Skipping {html_file}")
        else:
            print(f"Writing to {html_file}")
            with open(html_file, "w") as f:
                f.write(html)
                f.write("\n")

    if not over_write and os.path.exists(output_file):
        print(f"File already exists: {output_file}")
    else:
        output = {
            "metadata": {
                "title": "Schedule",
                "source": filename,
                "created": datetime.datetime.now().isoformat(),
            },
            "records": data
        }
        print(f"Writing to {output_file}")
        if not dry_run:
            with open(output_file, "w") as f:
                json.dump(output, f, default=str, indent=2)
                f.write("\n")
        else:
            print(json.dumps(output, default=str, indent=2))

    print("Done.")
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some files.")
    parser.add_argument("filename", type=str, help="The name of the file to process")
    parser.add_argument("--test", action="store_true", help="Enable dry run mode")
    parser.add_argument("--force", action="store_true", help="Force overwriting existing files")
    args = parser.parse_args()
    main(args.filename, args.test, args.force)