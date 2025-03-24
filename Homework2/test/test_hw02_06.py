import os
import re

def test_hw02_01():
    assert os.path.isfile('journalist_3.txt'), "Missing output file."
    lines = open('journalist_3.txt', 'r', encoding='utf-8').readlines()
    assert len(lines) > 0, "The file is empty."