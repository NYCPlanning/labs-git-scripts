# This script will remove the GitHub default labels and create custom labels for a repo

import csv
import requests
import sys

TOKEN = sys.argv[1]
REPO = sys.argv[2]
REPO_OWNER = 'NYCPlanning'
REPO_LIST = './csv/repos.txt'
HEADER = {'Authorization': 'token ' + TOKEN, 'Accept': 'application/vnd.github.symmetra-preview+json'}

TO_DELETE = ['bug',
    'duplicate',
    'enhancement',
    'help%20wanted',
    'good%20first%20issue',
    'invalid',
    'question',
    'wontfix',
    'documentation']

TO_CREATE = ['Sev1 Bug',
    'Sev2 Bug',
    'Sev3 Bug',
    'Sev4 Bug',
    'User: LUP',
    'User: Public',
    'User: Applicant',
    'Data Request',
    'Accessibility',
    'User Feedback',
    'New Feature',
    'Testing',
    'Refactor',
    'Performance',
    'DX',
    'Bug',
    'Critical Bug',
    'Blocked',
    'Design',
    'P1',
    'P2',
    'P3',
    'P4',
    'Strategic',
    'High ROI',
    'Easy Win',
    'Luxury',
    'DCP-QA',
    'Resolved',
    'Needs Clarification',
    'Greenskeeper']

DESC = ['Critical bug that entirely prevents use of the application',
    'Critical bug that entirely prevents use of a core feature',
    'Bug that prevents the use of a feature but has a workaround',
    'Minor bug that impacts UI/UX but doesn’t impact functionality',
    'Impacts ZAP LUP users',
    'Impacts ZAP public users',
    'Impacts ZAP applicant users',
    'Related to request for new data layers',
    'Related to improving accessibility for all users, including those with disabilities',
    'Feedback provided by a user',
    'Request for a new feature or new functionality',
    'Related to automated tests',
    'Related to refactoring code',
    'Enhancement that would improve app speed or performance',
    'Enhancement that would improve development experience',
    'Broken feature or unexpected behavior that negatively impacts the experience of using the app',
    'A critical, high priority bug that keeps users from being able to use the app',
    'An issue blocked by an external factor',
    'Requires design clarification or wireframes',
    'Priority 1 enhancement according to Product Owner',
    'Priority 2 enhancement according to Product Owner',
    'Priority 3 enhancement according to Product Owner',
    'Priority 4 enhancement according to Product Owner',
    'High impact, high level of effort. Used for work prioritization.',
    'High impact, low level of effort. Used for work prioritization.',
    'Low impact, low level of effort. Used for work prioritization.',
    'Low impact, high level of effort. Used for work prioritization.',
    'Applied for DCP-QA team for tracking purposes',
    'Applied by Labs to indicate that DCP-QA issues are ready for retesting',
    'Issue or user story is unclear. More info needed.',
    'To be handled by rotating, on-call Greenskeeper role']

COLORS = ['cb181d',
    'fb6a4a',
    'fcae91',
    'fee5d9',
    'e5df37',
    'e5df38',
    'e5df39',
    'aee5ef',
    'aee5ef',
    'aee5ef',
    'aee5ef',
    '92ad27',
    '92ad27',
    '92ad27',
    '92ad27',
    'd36315',
    'e21f18',
    '000000',
    'be81ea',
    '4B8AFF',
    '4B8AFF',
    '4B8AFF',
    '4B8AFF',
    '6600bb',
    '660066',
    'bb0066',
    'bb00bb',
    '36d8a2',
    '36d8a2',
    '3D3D3D',
    '378403']

# Delete GitHub's default labels
def delete_labels(repo):
    for i in TO_DELETE:
        DELETE_URL = 'https://api.github.com/repos/%s/%s/labels/%s' % (REPO_OWNER, repo, i)
        response = requests.delete(DELETE_URL, headers=HEADER)

# Create custom labels
def create_labels(repo):
    CREATE_URL = 'https://api.github.com/repos/%s/%s/labels' % (REPO_OWNER, repo)
    for j in range(len(TO_CREATE)):
        PARAMS = {"name":TO_CREATE[j], "description":DESC[j], "color":COLORS[j]}
        response = requests.post(CREATE_URL, json=PARAMS, headers=HEADER)


if REPO == 'all':
    with open(REPO_LIST) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count+=1
            else:
                repo_name = row[0]
                delete_labels(repo_name)
                create_labels(repo_name)
                line_count+=1
else:
    delete_labels(REPO)
    create_labels(REPO)
