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


def authorise(user, password):
    jira = "https://grit-jira.sanger.ac.uk"
    auth_jira = JIRA(jira, basic_auth=(user, password))
    return auth_jira


def tickets_new(auth_jira, week_no, proj):
    """
    Tickets that were created this week
    :param auth_jira:
    :param week_no:
    :param proj:
    :return:
    """
    if week_no == '-n':
        projects = auth_jira.search_issues(f'project="Assembly curation" AND '
                                           f'type {proj} AND created > startOfWeek() AND '
                                           f'created < endOfWeek()',
                                           maxResults=10000)
    else:
        projects = auth_jira.search_issues(f'project="Assembly curation" AND '
                                           f'type {proj} AND created > startOfWeek({week_no}) AND '
                                           f'created < endOfWeek({week_no})',
                                           maxResults=10000)

    print(f" ---- New Tickets ({proj})---- ")

    if len(projects) >= 1:
        for i in projects:
            issue = auth_jira.issue(f'{i}')
            print(f"{issue.fields.customfield_10201}\t{issue.fields.resolution}\t{issue.fields.created}")
    else:
        print("None")


def tickets_inprogress(auth_jira, week_no, proj):
    """
    Tickets that have been updated in the past week
    :param auth_jira:
    :param week_no:
    :param proj:
    :return:
    """

    # NEED TO ADD ABOUT IN SUBMISSION TOO
    if week_no == '-n':
        projects = auth_jira.search_issues(f'project="Assembly curation" AND type {proj} AND '
                                           f'resolution = "In progress" AND status != Submitted AND '
                                           f'status != "In Submission" AND updated > startOfWeek() AND '
                                           f'updated < endOfWeek()',
                                           maxResults=10000)
    else:
        projects = auth_jira.search_issues(f'project="Assembly curation" AND type {proj} AND '
                                           f'resolution = "In progress" AND status != Submitted AND '
                                           f'status != "In Submission" AND updated > startOfWeek({week_no}) AND '
                                           f'updated < endOfWeek({week_no})',
                                           maxResults=10000)

    print(f" ---- Inprogress Tickets ({proj})---- ")

    if len(projects) >= 1:
        for i in projects:
            issue = auth_jira.issue(f'{i}')
            print(f"{issue.fields.customfield_10201}\t{issue.fields.resolution}\t{issue.fields.updated}")
    else:
        print("None")


def tickets_submitted(auth_jira, week_no, proj):
    if week_no == '-n':
        projects = auth_jira.search_issues(f'project="Assembly curation" AND type {proj} AND '
                                           f'resolution = "In progress" AND status = Submitted OR '
                                           f'status = "In Submission" AND updated > startOfWeek() AND '
                                           f'updated < endOfWeek()')
    else:
        projects = auth_jira.search_issues(f'project="Assembly curation" AND type {proj} AND '
                                           f'resolution = "In progress" AND status = Submitted OR '
                                           f'status = "In Submission" AND updated > startOfWeek({week_no}) AND '
                                           f'updated < endOfWeek({week_no})')

    print(f" ---- Submitted/Insubmission Tickets ({proj})---- ")

    if len(projects) >= 1:
        for i in projects:
            issue = auth_jira.issue(f'{i}')
            print(f"{issue.fields.customfield_10201}\t{issue.fields.resolution}\t{issue.fields.updated}")
    else:
        print("None")
    pass


def main():
    project_list = ['= "Darwin"', '!= "Darwin"']
    week_no = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]

    auth_jira = authorise(username, password)

    for proj in project_list:
        tickets_new(auth_jira, week_no, proj)
        tickets_inprogress(auth_jira, week_no, proj)
        tickets_submitted(auth_jira, week_no, proj)


if __name__ == "__main__":
    main()


