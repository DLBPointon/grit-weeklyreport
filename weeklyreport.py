"""
Welcome to the Weekly Report for Jira in GRIT
by dp24

Pulls
Weekly data split by project
    - Tickets new
    - Tickets modified
    - Tickets Finished
All within a specified week.

REQUIRES:
- jira

Usage:
    - For most recent week report
python3 weeklyreport.py -n

    - For one week in the past
python3 weeklyreport.py -1w

    - Two weeks would be
python3 weeklyreport.py -2w

    - Output to TSV with:
python3 weeklyreport.py -1w > {TITLE}.tsv

"""
import sys
from jira import JIRA
import os
from dotenv import load_dotenv
import datetime
import maya


def dotloader():
    load_dotenv()
    jira_user = os.getenv('JIRA_USER')
    jira_pass = os.getenv('JIRA_PASS')
    return jira_user, jira_pass


def authorise(user, password):
    jira = "https://grit-jira.sanger.ac.uk"
    auth_jira = JIRA(jira, basic_auth=(user, password))
    return auth_jira


def tickets_new(auth_jira, week_no, proj, queue):
    """
    Tickets that were created this week
    :param queue:
    :param auth_jira:
    :param week_no:
    :param proj:
    :return:
    """
    if week_no == '-n':
        projects = auth_jira.search_issues(f'project={queue} AND '
                                           f'type {proj} AND '
                                           f'created > startOfWeek() AND '
                                           f'created < endOfWeek()',
                                           maxResults=10000)
    else:
        projects = auth_jira.search_issues(f'project={queue} AND '
                                           f'type {proj} AND '
                                           f'created > startOfWeek({week_no}) AND '
                                           f'created < endOfWeek({week_no})',
                                           maxResults=10000)

    print(f" ---- New Tickets ({queue}: {proj})---- ")

    if len(projects) >= 1:
        for i in projects:
            issue = auth_jira.issue(f'{i}')
            obj = maya.parse(issue.fields.created).datetime()
            ymd_date = obj.date().strftime('%Y-%m-%d')
            print(f"{issue.fields.customfield_10201}\t"
                  f"{issue.fields.issuetype.name}\t"
                  f"{issue.fields.resolution}\t"
                  f"{ymd_date}\t"
                  f"{issue.fields.status}")
    else:
        print("None")


def tickets_inprogress(auth_jira, week_no, proj, queue):
    """
    Tickets that have been updated in the past week
    :param queue:
    :param auth_jira:
    :param week_no:
    :param proj:
    :return:
    """

    # NEED TO ADD ABOUT IN SUBMISSION TOO
    if week_no == '-n':
        if queue == '"Rapid Curation"':
            projects = auth_jira.search_issues(f'project={queue} AND '
                                               f'type {proj} AND '
                                               f'resolution = "Unresolved" AND '
                                               f'status != "Submitted" AND '
                                               f'updated > startOfWeek() AND '
                                               f'updated < endOfWeek()',
                                               maxResults=10000)
        else:
            # This doesn't use datetime stuff at all on purpose,
            # if it did it would remove tickets that are not updated at least once per week.
            projects = auth_jira.search_issues(f'project={queue} AND '
                                               f'type {proj} AND '
                                               f'resolution = "In progress" AND '
                                               f'status != "Submitted" AND '
                                               f'updated > startOfWeek() AND '
                                               f'updated < endOfWeek()',
                                               maxResults=10000)
    else:
        if queue == '"Rapid Curation"':
            projects = auth_jira.search_issues(f'project={queue} AND '
                                               f'type {proj} AND '
                                               f'resolution = "Unresolved" AND '
                                               f'status != "Submitted" AND '
                                               f'updated > startOfWeek({week_no}) AND '
                                               f'updated < endOfWeek({week_no})',
                                               maxResults=10000)
        else:
            projects = auth_jira.search_issues(f'project={queue} AND '
                                               f'type {proj} AND '
                                               f'resolution = "In progress" AND '
                                               f'status != "Submitted" AND '
                                               f'updated > startOfWeek({week_no}) AND '
                                               f'updated < endOfWeek({week_no})',
                                               maxResults=10000)

    print(f" ---- Inprogress Tickets ({queue}: {proj}) ---- ")

    if len(projects) >= 1:
        for i in projects:
            issue = auth_jira.issue(f'{i}')
            obj = maya.parse(issue.fields.updated).datetime()
            ymd_date = obj.date().strftime('%Y-%m-%d')
            print(f"{issue.fields.customfield_10201}\t"
                  f"{issue.fields.issuetype.name}\t"
                  f"{issue.fields.resolution}\t"
                  f"{ymd_date}\t"
                  f"{issue.fields.status}")
    else:
        print("None")


def tickets_submitted(auth_jira, week_no, proj, queue):
    if week_no == '-n':
        projects = auth_jira.search_issues(f'project={queue} AND '
                                           f'type {proj} AND '
                                           f'status = Submitted AND status = "In Submission" AND '
                                           f'updated > startOfWeek() AND '
                                           f'updated < endOfWeek()')
    else:
        projects = auth_jira.search_issues(f'project={queue} AND '
                                           f'type {proj} AND '
                                           f'status = Submitted AND status = "In Submission" AND '
                                           f'updated > startOfWeek({week_no}) AND '
                                           f'updated < endOfWeek({week_no})')

    print(f" ---- Submitted Tickets ({queue}: {proj})---- ")

    if len(projects) >= 1:
        for i in projects:
            issue = auth_jira.issue(f'{i}')
            obj = maya.parse(issue.fields.updated).datetime()
            ymd_date = obj.date().strftime('%Y-%m-%d')
            print(f"{issue.fields.customfield_10201}\t"
                  f"{issue.fields.issuetype.name}\t"
                  f"{issue.fields.resolution}\t"
                  f"{ymd_date}\t"
                  f"{issue.fields.status}")
    else:
        print("None")
    pass


def main():
    # ASG will need to be added once in use. - 3, '!= "ASG" AND != "Darwin"'
    queue_list = ['"Rapid Curation"', '"Assembly curation"']
    project_list = ['= "Darwin"', '= "VGP"', '= "VGP+"', '= "ASG"', '= "ERGA"', '= "Faculty"', '= "Other"']

    username, password = dotloader()
    week_no = sys.argv[1]

    auth_jira = authorise(username, password)

    print(f'============== START for {datetime.date.today()} ============')
    for i in queue_list:
        for proj in project_list:
            tickets_new(auth_jira, week_no, proj, i)
            tickets_inprogress(auth_jira, week_no, proj, i)
            tickets_submitted(auth_jira, week_no, proj, i)
        print('================ QUEUE BREAK ================')
    print(f'============== END for {datetime.date.today()} =============')


if __name__ == "__main__":
    main()
