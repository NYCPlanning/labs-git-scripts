# This script will create a milestone across all repos and boards

import csv
import requests
import itertools

TOKEN = 'e633eaf50861324a34ba878f7fb6161a94c6dd7f'
REPO_OWNER = 'NYCPlanning'
#REPO_NAME = 'labs-zola'
HEADER = {'Authorization': 'token ' + TOKEN}

f1 = open('test-repos.txt')
f2 = open('sprints.txt')

csv_f1 = csv.reader(f1, delimiter=',')
csv_f2 = csv.reader(f2, delimiter=',')

line_count = 0
for row in csv_f1: 
        if line_count == 0:
                line_count+=1
        else:
                repo_name = row[0]

line_count = 0
for row2 in csv_f2:
        if line_count == 0:
                line_count+=1
        else:
                # Set milestone
                title = row2[0]
                due_on = row2[1]
                url = 'https://api.github.com/repos/%s/%s/milestones' % (REPO_OWNER, repo_name)
                params = {"title":title, "due_on":due_on}
                response = requests.post(url, json=params, headers=HEADER)
                line_count+=1
