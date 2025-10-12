#!/bin/dash
# Script to take yahoo!finance daily history data table and convert to CSV of date and average value
# stdin: table html
# stdout: csv
#
# Note: Table needs to be copied via a human through inspect element
# DEPRECATED by yahoo.py

# Extract `tr` HTML entries
sed -E 's:</([^>]*)>:<\1>\n:g' | sed -E 's:^.*">([^<]*)<.*$:\1:g' |
  # Looking for lines that start with a month or number
  grep '^[A-Z0-9]' | tr '\n' '\t' | sed -E 's:([A-Z]):\n\1:g' |
  # Some entries just mention dividends; exclude
  grep '\t.*\t.*\t' |
  # Average the openings, closings, etc.
  awk -F\t '{print $1, ($2 + $3 + $4 + $5 + $6)/5}' |
  # Format the dates to DD/MM/YYYY
  sed -E 's/([0-9]{4}) /\1,/' | sed -E 's/^([A-Za-z]{3}) ([0-9]{1,2}),(.*)/\2 \1\3/' | sed 's: Jan :/01/:; s: Feb :/02/:; s: Mar :/03/:; s: Apr :/04/:; s: May :/05/:; s: Jun :/06/:; s: Jul :/07/:; s: Aug :/08/:; s: Sep :/09/:; s: Oct :/10/:; s: Nov :/11/:; s: Dec :/12/:' | sed -E 's:^([0-9]/):0\1:' |
  # Put into chronological order
  tac |
  # Add CSV headings to make them valid
  awk 'BEGIN {print "Date,Value"} {print}'

