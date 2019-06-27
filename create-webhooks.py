# This script will create a hubot webhook across all existing Labs repos

import csv
import os
import requests
from dotenv import load_dotenv

load_dotenv()
REPO_LIST = './csv/repos.txt'
REPO_OWNER = 'NYCPlanning'
TOKEN = os.environ['GITHUB_PERSONAL_ACCESS_TOKEN']
HEADER = {'Authorization': 'token ' + TOKEN, 'Accept': 'application/vnd.github.symmetra-preview+json'}
CONFIG = {"url":"http://plannerbot.planninglabs.nyc/hubot/github-repo-listener"}

def create_repo_hook(repo):
    url = 'https://api.github.com/repos/%s/%s/hooks' % (REPO_OWNER, repo)
    # webhook triggered by all repo events (creation, renamed, etc.)
    events = ['repository']
    params = {"config":CONFIG, "events":events}
    response = requests.post(url, json=params, headers=HEADER)

def create_push_hook(repo):
    url = 'https://api.github.com/repos/%s/%s/hooks' % (REPO_OWNER, repo)
    # webhook triggered by push to a repo
    events = ['push']
    params = {"config":CONFIG, "events":events}
    response = requests.post(url, json=params, headers=HEADER) 


with open(REPO_LIST) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count+=1
        else:
            repo_name = row[0]
            create_repo_hook(repo_name)
            create_push_hook(repo_name)
            line_count+=1