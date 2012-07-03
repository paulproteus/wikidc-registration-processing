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
    if datum['Status'].lower() == 'completed':
        out_dicts.append(datum)

out_writer = csv.DictWriter(sys.stdout, fieldnames = out_dicts[0].keys())
out_writer.writerow(dict((f,f) for f in out_writer.fieldnames) )

for datum in out_dicts:
    out_writer.writerow(datum)
