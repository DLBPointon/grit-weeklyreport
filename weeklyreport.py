"""
Welcome to the Weekly Report for Jira in GRIT
by dp24

Pulls
Weekly data.

New tickets come in.    - Date
tickets in progress (any status not open, submitted or done) - Status
tickets at submitted - Submitted
split Darwin, ASG, other - project_type

Usage:
    - For most recent week report
python3 weeklyreport.py

    - For one week in the past
python3 weeklyreport.py -1w {USER} {PASS}

    - Two weeks would be
python3 weeklyreport.py -2w {USER} {PASS}

    - Output to TSV with:
python3 weeklyreport.py -1w {USER} {PASS} > {TITLE}.tsv
"""
import sys
from jira import JIRA

jira = "https://grit-jira.sanger.ac.uk"
auth_jira = JIRA(jira, basic_auth=(sys.argv[2], sys.argv[3]))
if sys.argv[1] == '-n':
    projects = auth_jira.search_issues(
        f'project="Assembly curation" AND created > startOfWeek() AND created < endOfWeek()',
        maxResults=10000)
else:
    projects = auth_jira.search_issues(
        f'project="Assembly curation" AND created > startOfWeek({sys.argv[1]}) AND created < endOfWeek({sys.argv[1]})',
        maxResults=10000)


for i in projects:
    issue = auth_jira.issue(f'{i}')
    summary = issue.fields.summary

    # Prints Project_id (ilNocJant1), Project_type (Darwin, VGP etc), Status, Current resolution, ticket creation date
    print(f"{issue.fields.customfield_10201}\t{issue.fields.issuetype}\t{issue.fields.status}"
          f"\t{issue.fields.resolution}\t{issue.fields.created}")