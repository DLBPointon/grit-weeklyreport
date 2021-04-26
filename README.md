Welcome to the Weekly Report for Jira in GRIT
by dp24

Pulls data in weekly increments.
TolID /t Project_id /t Status of Ticket /t Current Resolution /t Date of Ticket Creation

Usage:
- For most recent week report

`python3 weeklyreport.py`

- For one week in the past

`python3 weeklyreport.py -1w {USER} {PASS}`

- Two weeks would be

`python3 weeklyreport.py -2w {USER} {PASS}`

- Output to TSV with:

`python3 weeklyreport.py -1w {USER} {PASS} > {TITLE}.tsv`

REQUIRMENTS
This does require the jira module:
`pip install jira`

