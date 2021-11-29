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
import os
from dotenv import load_dotenv
from datetime import date


def dotloader():
    load_dotenv()
    jira_user = os.getenv('JIRA_USER')
    jira_pass = os.getenv('JIRA_PASS')
    return jira_user, jira_pass


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


def get_info(auth_jira, queue, search_string, project):
    projects = auth_jira.search_issues(search_string,
                                       maxResults=10000)

    i = ''
    length_after = None
    length_before = None

    print(f' --- {queue}: {project} --- ')
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
    proj = ''
    queue_code = ['"Rapid Curation"', '"Assembly curation"']
    project_list = ['= "Darwin"', '= "VGP"', '= "VGP+"', '= "ASG"', '= "ERGA"', '= "Faculty"', '= "Other"']
    username, password = dotloader()

    auth_jira = authorise(username, password)

    print(f'============== START for {date.today()} ============')
    for i in queue_code:
        for ii in project_list:
            proj_search = f'project={i} AND type {ii} AND status IN ("In Submission", "Submitted", "Post Processing++")'
            get_info(auth_jira, i, proj_search, ii)
        print('================ QUEUE BREAK ================')
    print(f'============== END for {date.today()} =============')


if __name__ == '__main__':
    main()
