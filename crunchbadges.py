#!/usr/bin/python3
# coding=UTF-8
# Crunch brain-dead CSV output from Drupal for Wikimania 2012 badges
# ©2012 Fran McCrory, all hail GNU/dad!
#
# Usage: crunchbadges.py <old.csv >new.csv

import csv
import sys

# Burn off first line; we don't need the old column names
sys.stdin.readline()

# Read stdin as a CSV file
csv_in = csv.reader(sys.stdin)

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
    dict_row = {"Uid":                row[0],
                "Order ID":           row[1],
                "Order product ID":   row[2],
                "Payer's first name": row[3],
                "Payer's last name":  row[4],
                "Status":             row[5]}
  
    # Split lines of attributes column, filtering out blanks
    attr_lines = filter(lambda s: len(s) != 0,
                        row[6].splitlines())

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
csv_out = csv.writer(sys.stdout)

# Print out a row for the column headings
csv_out.writerow(column_names)

# Now, print out the rows
for dict_row in dict_rows:
    # Order the columns in the order we encountered them
    columns = []
    for column_name in column_names:
        # Output the column, or "" if it doesn't exist on this row
        if column_name in dict_row:
            columns.append(dict_row[column_name])
        else:
            columns.append("");

    # Write out the row
    csv_out.writerow(columns)
