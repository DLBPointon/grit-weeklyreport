Welcome to the Jira Scripts for GRIT
by dp24

REQUIRMENTS
This does require the jira module as well as dotenv:

`pip install jira`

`pip install python-dotenv`

Other modules should be pre-installed with python.

## weeklyreport.py
This script pulls weekly data split by project, and further split by:
    - Tickets new
    - Tickets modified
    - Tickets Finished

Usage:
- For most recent week report

`python3 weeklyreport.py -n`

- For one week in the past

`python3 weeklyreport.py -1w`

- Two weeks would be

`python3 weeklyreport.py -2w`

- Output to TSV with:

`python3 weeklyreport.py -1w > {TITLE}.tsv`

Results example:
weekly14052021.tsv

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

Usage:

`- python3 manual_report.py`

`- python3 manual_report.py > {SOMETHING}.tsv`

Results example:

manual14052021.tsv