# This script will create a hubot webhook across all existing Labs repos

import csv
import os
from dotenv import load_dotenv
load_dotenv()

REPO_LIST = './csv/repos.txt'
REPO_OWNER = 'NYCPlanning'
TOKEN = os.environ['GITHUB_PERSONAL_ACCESS_TOKEN']
HEADER = {'Authorization': 'token ' + TOKEN, 'Accept': 'application/vnd.github.symmetra-preview+json'}


# def create_hook(repo):
# 	CREATE_URL = 'https://api.github.com/repos/%s/%s/labels' % (REPO_OWNER, repo)
#     PARAMS = {"name":TO_CREATE[j], "description":DESC[j], "color":COLORS[j]}
#     response = requests.post(CREATE_URL, json=PARAMS, headers=HEADER)

# with open(REPO_LIST) as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         if line_count == 0:
#             line_count+=1
#         else:
#             repo_name = row[0]
#             delete_labels(repo_name)
#             create_labels(repo_name)
#             line_count+=1