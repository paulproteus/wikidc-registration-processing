#!/usr/bin/python3
# coding=UTF-8
# Crunch brain-dead CSV output from Drupal for Wikimania 2012 badges
# ©2012 Fran McCrory, all hail GNU/dad!
#
# Usage: crunchbadges.py <old.csv >new.csv

import csv
import sys

# Read stdin as a CSV file
csv_in = csv.DictReader(sys.stdin)

# This list will collect all column names it encounters.
column_names = ["Uid",
                "Order ID",
                "Order product ID",
                "Payer's first name",
                "Payer's last name",
                "Status"]

# Process the incoming rows
dict_rows = []
for row in csv_in:
    # Create an initial dict for the first six columns
    dict_row = {"Uid":                row["Uid"],
                "Order ID":           row["Order ID"],
                "Order product ID":   row["Order product ID"],
                "Payer's first name": row["Payer's first name"],
                "Payer's last name":  row["Payer's last name"],
                "Status":             row["Status"],
    }
  
    # Split lines of attributes column, filtering out blanks
    attr_lines = filter(lambda s: len(s) != 0,
                        row['Ordered product attributes'].splitlines())

    # Stick each attribute into its corresponding column
    for line in attr_lines:
        key, sep, value = line.partition(': ')
        if key != "":
            dict_row[key] = value

            # Add the attribute name to our column names if necessary
            if key not in column_names:
                column_names.append(key)

    # Done with this row
    dict_rows.append(dict_row)

# Write to stdout as a CSV
csv_out = csv.DictWriter(sys.stdout, column_names)

## Print out a row for the column headings
csv_out.writeheader()

# Now, print out the rows
for dict_row in dict_rows:
    csv_out.writerow(dict_row)
