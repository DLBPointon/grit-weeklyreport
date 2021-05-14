Welcome to the Jira Scripts for GRIT
by dp24


## weeklyreport.py
This script pulls weekly data split by project, and further split by:
    - Tickets new
    - Tickets modified
    - Tickets Finished

Usage:
- For most recent week report

`python3 weeklyreport.py -n {USER} {PASS}`

- For one week in the past

`python3 weeklyreport.py -1w {USER} {PASS}`

- Two weeks would be

`python3 weeklyreport.py -2w {USER} {PASS}`

- Output to TSV with:

`python3 weeklyreport.py -1w {USER} {PASS} > {TITLE}.tsv`

REQUIRMENTS
This does require the jira module:
`pip install jira`

## manual_report.py
Manual Interventions Reporting in GRIT
by dp24

Pulls data for:
- Project
- TolID
- Manual Breaks
- Manual Joins
- Manual Haplotype Removals
- Assembly Size - From Assembly Stats section

Ordered by Project

REQUIRES:
- jira
- re

Usage:

`- python3 manual_report {USER} {PASSWORD}`

`- python3 manual_report {USER} {PASSWORD} > {SOMETHING}.tsv`