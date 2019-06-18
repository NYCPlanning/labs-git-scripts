# This script will move issues between pipelines on a ZenHub board

# note: code assumes naming convention for branches and PRs is 123-.... with 123 being the corresponding issue #

import csv
import json
import requests

IN_PROGRESS = 4
REVIEW = 5
STAGING = 6

GTOKEN = sys.argv[1]
ZTOKEN = sys.argv[2]
REPO_OWNER = 'NYCPlanning'
GIT_HEADER = {'Authorization': 'token ' + GTOKEN}
ZEN_HEADER = {'X-Authentication-Token': ZTOKEN}

with open('test-repos.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
                line_count+=1
        else:
            repo_name = row[0]

            # get repo id
            repo_url = 'https://api.github.com/repos/%s/%s' % (REPO_OWNER, repo_name)
            repo_response = requests.get(repo_url, headers=GIT_HEADER)
            repo_data = json.loads(repo_response.text)
            repo_id = repo_data['id']

            # get branches data
            branch_url = 'https://api.github.com/repos/%s/%s/branches' % (REPO_OWNER, repo_name)
            branch_response = requests.get(branch_url, headers=GIT_HEADER)
            branch_data = json.loads(branch_response.text)
            branches = []
            for i, item in enumerate(branch_data):
                    branches.append(branch_data[i]['name'].split('-')[0])

            # get issues data
            issue_url = 'https://api.github.com/repos/%s/%s/issues' % (REPO_OWNER, repo_name)
            issue_response = requests.get(issue_url, headers=GIT_HEADER)
            issue_data = json.loads(issue_response.text)
            issues = []
            for j, item in enumerate(issue_data):
                    issues.append(issue_data[j]['number'])

            # get pull requests data
            pr_url = 'https://api.github.com/repos/%s/%s/pulls' % (REPO_OWNER, repo_name)
            pr_response = requests.get(pr_url, headers=GIT_HEADER)
            pr_data = json.loads(pr_response.text)
            pulls = []
            for k, item in enumerate(pr_data):
                    pulls.append(pr_data[k]['title'].split(':')[0])

            # get board data
            board_url = 'https://api.zenhub.io/p1/repositories/%s/board' % (repo_id)
            board_response = (requests.get(board_url, headers=ZEN_HEADER))
            board_data = json.loads(board_response.text)
            in_progress_id = board_data['pipelines'][IN_PROGRESS]['id']
            review_id = board_data['pipelines'][REVIEW]['id']
            staging_id = board_data['pipelines'][STAGING]['id']


            # move issue to 'In Progress' if it corresponds to a feature branch
            for l in issues:
                    if str(l) in branches:
                            url = 'https://api.zenhub.io/p1/repositories/%s/issues/%d/moves' % (repo_id, l)
                            params = {'pipeline_id':in_progress_id, 'position':'bottom'}
                            response = requests.post(url, json=params, headers=ZEN_HEADER)

            # move issue to 'Review/QA' if PR has been opened
            for m in issues:
                    if str(m) in pulls:
                            url= 'https://api.zenhub.io/p1/repositories/%s/issues/%d/moves' % (repo_id, m)
                            params = {'pipeline_id':review_id, 'position':'bottom'}
                            response = requests.post(url, json=params, headers=ZEN_HEADER)

            # move issue to 'Staging' if PR has been merged into develop
            for n in pulls:
                    url = 'https://api.github.com/repos/%s/%s/pulls/%d/merge' % (REPO_OWNER, repo_id, int(n))
                    response = requests.get(url, headers=GIT_HEADER)
                    # check if PR has been merged
                    print(response.status_code)
                    if (200 <= response.status_code  <= 200):
                            url = 'https://api.zenhub.io/p1/repositories/%s/issues/%d/moves' % (repo_id, n)
                            params = {'pipeline_id':STAGING_id, 'position':'bottom'}
                            response = requests.post(url, json=params, headers=ZEN_HEADER)
                            print(response.status_code)
  