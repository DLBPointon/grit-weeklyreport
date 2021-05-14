"""
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
    - python3 manual_report {USER} {PASSWORD}

    - python3 manual_report {USER} {PASSWORD} > {SOMETHING}.tsv
"""

import sys
from jira import JIRA
import re


def authorise(user, password):
    jira = "https://grit-jira.sanger.ac.uk"
    auth_jira = JIRA(jira, basic_auth=(user, password))
    return auth_jira


def reg_length_info(scaff_data):
    """
    Function to return the length information hidden in assembly stats
    :param issue < ticket:
    :return:
    """
    length_before = None
    length_after = None

    if isinstance(scaff_data, str):
        length_search = re.search(r'total\s*([0-9]\w+)\s*([0-9]\w+)', scaff_data)
        if length_search:
            length_before = int(length_search.group(1))
            length_after = int(length_search.group(2))
        else:
            length_after = 'NOT AVAILABLE'
            length_before = 'NOT AVAILABLE'
    else:
        pass

    return length_before, length_after


def get_info(auth_jira, proj):

    projects = auth_jira.search_issues(f'project="Assembly curation" AND '
                                       f'type {proj} AND '
                                       f'status = "In Submission" OR '
                                       f'project="Assembly curation" AND '
                                       f'type {proj} AND '
                                       f'status = "Submitted" OR '
                                       f'project="Assembly curation" AND '
                                       f'type {proj} AND '
                                       f'status = "Post Processing++"',
                                       maxResults=10000)

    i = ''
    length_after = None
    length_before = None

    print(f' --- {proj} --- ')
    print(f'TOLID\tBREAKS\tJOINS\tHAP_REMOVE\tASSEMBLY_LENGTH_AC')

    for i in projects:
        issue = auth_jira.issue(f'{i}')
        tolid = issue.fields.customfield_10201
        scaff_data = issue.fields.customfield_10226
        breaks = issue.fields.customfield_10219
        joins = issue.fields.customfield_10220
        haprm = issue.fields.customfield_10222

        length_before, length_after = reg_length_info(scaff_data)
        print(f'{tolid}\t{breaks}\t{joins}\t{haprm}\t{length_after}')


def main():
    project_list = ['= "Darwin"', '= "VGP+"', '= "VGP orders"']
    username = sys.argv[1]
    password = sys.argv[2]

    auth_jira = authorise(username, password)

    for proj in project_list:
        get_info(auth_jira, proj)


if __name__ == '__main__':
    main()