#!/usr/bin/env python
# -*- coding: utf-8 -*-

# based on https://stackoverflow.com/a/16954837

import argparse
import functools
import heapq
import os
import tempfile

parser = argparse.ArgumentParser(description="Sort GameTracking VPK summaries")
parser.add_argument("file", type=str)
args = parser.parse_args()
file_name = args.file


def size_sort(line):
    return int(line.split("size:")[1])


sorted_files = []
num_bytes = 1 << 20

with open(file_name) as file:
    for lines in iter(functools.partial(file.readlines, num_bytes), []):
        lines.sort(key=size_sort)
        f = tempfile.TemporaryFile("w+")
        f.writelines(lines)
        f.seek(0)
        sorted_files.append(f)

base_path, ext = os.path.splitext(file_name)
sorted_file_name = base_path + "_sorted" + ext

with open(sorted_file_name, "w+") as file:
    file.writelines(heapq.merge(*sorted_files, key=size_sort))

for f in sorted_files:
    f.close()
