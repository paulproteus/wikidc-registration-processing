#!/usr/bin/python3
# coding=UTF-8
# Written by Asheesh. (C) OpenHatch Foundation, Inc.
# Permission to use granted under the GPLv3 or any license
# you ask me about.

import csv
import sys

in_data = csv.DictReader(sys.stdin)
out_dicts = []
for datum in in_data:
    days = datum['Days attending'].lower()
    if 'eveloper' in days:
        out_dicts.append(datum)

out_writer = csv.DictWriter(sys.stdout, fieldnames = out_dicts[0].keys())
out_writer.writeheader()
for datum in out_dicts:
    out_writer.writerow(datum)
