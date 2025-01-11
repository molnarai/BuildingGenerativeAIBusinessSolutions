#!/usr/bin/env python3
TITLE = r"""
  _____ _         ____ _ _        _   _                 
 |  ___(_)_  __  / ___(_) |_ __ _| |_(_) ___  _ __  ___ 
 | |_  | \ \/ / | |   | | __/ _` | __| |/ _ \| '_ \/ __|
 |  _| | |>  <  | |___| | || (_| | |_| | (_) | | | \__ \
 |_|   |_/_/\_\  \____|_|\__\__,_|\__|_|\___/|_| |_|___/
                                                        
"""
import os
import sys
import re
import argparse

def main(filename: str, pipe: bool = False):
    with open(filename, "r") as f:
        lines = f.readlines()

    # citation_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    citation_pattern = re.compile(r"^\[(\d+)\]\s+(http.+)")

    citation_line = 99999
    citations = {}
    for j, line in enumerate(lines):
        if m := citation_pattern.match(line.strip()):
            citations[m.group(1)] = m.group(2)
            citation_line = min(j, citation_line)

    # fix citations
    for i in range(citation_line):
        for k, v in citations.items():
            lines[i] = lines[i].replace(f"[{k}]", f"""<a href="{v}" target="_blank">[{k}]</a>""")

    if pipe:
        for j, line in enumerate(lines):
            if j == citation_line-1:
                print("## Citations")
            elif j > citation_line-1:
                print("- " + line, end="") 
            else:
                print(line, end="")
    else:
        with open(filename, "w") as f:
            for j, line in enumerate(lines):
                if j == citation_line-1:
                    f.write("## Citations\n")
                elif j > citation_line-1:
                    f.write("- " + line)
                else:
                    f.write(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=TITLE)
    parser.add_argument("filename", help="Markdown file to fix")
    parser.add_argument("--pipe", "-p", action="store_true", help="Send output to STDIOUT")
    args = parser.parse_args()
    main(args.filename, args.pipe)