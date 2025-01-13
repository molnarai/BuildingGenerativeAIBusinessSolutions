#!/usr/bin/env python3

"""
A simple script to convert a single input bib-file to BibJSON output that is send to stdout.
"""

import sys
import bibjson
import os
import json
from datetime import datetime


def convert_to_initials(comma_sep_name):
    """_summary_

    Args:
        comma_sep_name (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        lastname, firstname = tuple(comma_sep_name.split(',', 1))
        initials = ' '.join([ "{}.".format(t[0].upper()) for t in firstname.strip().split(' ') ])
        return f"{lastname.strip()}, {initials}"
    except:
        return comma_sep_name


def main():
    """
    Script main function: Read arguments, produce BibJSON output.
    """
    if len(sys.argv) < 2:
        print("will output BibJSON to stdout", file=sys.stderr)
        print("usage: %s <bibtex-file>" % sys.argv[0], file=sys.stderr)
        exit(1)

    bibtex_file = sys.argv[1]

    # 'collection' identifier is the file name without extension
    collection = os.path.splitext(os.path.basename(bibtex_file))[0]

    # read the bibtex file
    with open(bibtex_file) as f:
        bibtex_str = f.read()

        # create BibJSON collection from file
        bibjson_collection = bibjson.collection_from_bibtex_str(bibtex_str,
                                                                collection=collection,
                                                                source=bibtex_file,
                                                                created=datetime.utcnow().isoformat())

        # Fix Authors and Editors for APA style ()
        bibjson_collection2 = {
            "metadata": bibjson_collection.get("metadata", {}),
            "records": []
        }
        for rec in bibjson_collection['records']:
            new_authors = []
            if "author" in rec.keys():
                for author in rec["author"]:
                    if "name" in author.keys():
                        new_authors.append({"name": convert_to_initials(author["name"])})
            rec["author"] = new_authors
            bibjson_collection2["records"].append(rec)

        # print it to stdout with nice indentation
        json.dump(bibjson_collection2, sys.stdout, indent=True)


if __name__ == '__main__':
    main()
