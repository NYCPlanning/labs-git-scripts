# This script will create a hubot webhook across all existing Labs repos

# import csv

# REPO_LIST = './csv/repos.txt'

# with open(REPO_LIST) as csv_file:
#         csv_reader = csv.reader(csv_file, delimiter=',')
#         line_count = 0
#         for row in csv_reader:
#             if line_count == 0:
#                 line_count+=1
#             else:
#                 repo_name = row[0]
#                 delete_labels(repo_name)
#                 create_labels(repo_name)
#                 line_count+=1