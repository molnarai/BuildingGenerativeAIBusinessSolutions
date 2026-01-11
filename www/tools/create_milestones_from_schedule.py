#!/usr/bin/env python
TITLE = r'''
  __  __ _ _           _                        
 |  \/  (_) | ___  ___| |_ ___  _ __   ___  ___ 
 | |\/| | | |/ _ \/ __| __/ _ \| '_ \ / _ \/ __|
 | |  | | | |  __/\__ \ || (_) | | | |  __/\__ \
 |_|  |_|_|_|\___||___/\__\___/|_| |_|\___||___/
                                                
'''
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
    schedule_df = pd.read_excel(filename)
    columns_to_keep = ["Session", "Monday", "Wednesday", "Topic", "InClass", "Milestone"]
    available_columns = [col for col in columns_to_keep if col in schedule_df.columns]
    schedule_df = schedule_df[available_columns]
    schedule_df['Session'] = schedule_df['Session'].map(lambda x: str(int(float(x))) if x != "" else "", na_action="ignore")
    schedule_df = schedule_df.fillna("")
    milestones = schedule_df.Milestone.dropna().values

    milestone_data = []
    for milestone in milestones:
        if not milestone or milestone == "":
            continue
        # Extract milestone name
        match = re.match(r'(M\d+[^.]*)', milestone)
        if not match:
            continue
        name = match.group(1)
        
        # Extract dates
        mon_match = re.search(r'Monday: due ([^;]+)', milestone)
        wed_match = re.search(r'Wednesday: due ([^)]+)', milestone)
        
        monday = mon_match.group(1) if mon_match else ""
        wednesday = wed_match.group(1) if wed_match else ""
        
        milestone_data.append({'Milestone': name, 'Monday': monday, 'Wednesday': wednesday})

    milestone_df = pd.DataFrame(milestone_data)

    data = milestone_df.to_dict(orient='records')
    markdown = milestone_df.rename(lambda s: s.replace(' ', ''), axis=1).to_markdown(index=False)
    html = milestone_df.to_html(index=False, classes="table table-striped table-hover")

    output_file = jp(WWW_DIR, "data", "milestones_schedule.json")
    html_file = jp(WWW_DIR, "content", "milestones_schedule.html")
    markdown_file = jp(WWW_DIR, "content", "milestones_schedule.md")
    tex_file = jp(WWW_DIR, "static", "files", "milestones_schedule.tex")

    if not dry_run:
        ###
        ### Markdown

        if not over_write and os.path.exists(markdown_file):
            print(f"Skipping {markdown_file}")
        else:
            print(f"Writing to {markdown_file}")
            with open(markdown_file, "w") as f:
                f.write(markdown)
                f.write("\n")
        
        ###
        ### HTML
        ###
        if not over_write and os.path.exists(html_file):
            print(f"Skipping {html_file}")
        else:
            print(f"Writing to {html_file}")
            with open(html_file, "w") as f:
                f.write(html)
                f.write("\n")
        
        ###
        ### Tex
        ###
        if not over_write and os.path.exists(tex_file):
            print(f"Skipping {tex_file}")
        else:
            amp = chr(38)  # ASCII ampersand
            with open(tex_file, "w", encoding='utf-8') as io:
                for i, row in milestone_df.iterrows():
                    io.write(f"{row.Milestone} {amp} {row.Monday} {amp} {row.Wednesday}  \\\\\n")

        ###
        ### JSON
        ###
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