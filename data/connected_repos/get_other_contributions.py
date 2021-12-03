import pandas as pd
import requests
from github import Github
import pickle

access_token='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'
headers = {'Authorization':"Token "+access_token} # we need header to obtain more data

def collect_data(usernames):
    # set up user name we want to research and get your own access_token , then create header
    user_repos = {}
    for user in usernames:
        entry_per_page = 100
        pg_num = 1
        all_repos = []
        user_repos[user] = []
        while entry_per_page > 0:
            url = f"https://api.github.com/users/blink1073/repos?page={pg_num}&per_page=100"
            repos = requests.get(url,headers=headers).json()
            pg_num += 1
            entry_per_page = len(repos)
            for repo in repos:

                if repo['private'] == False and repo['fork'] == True and repo['language'] == 'Python':
                    print('')
                    print(repo['full_name'])
                    if repo['private'] == False:
                        print('it is not private')
                    if repo['fork'] == True:
                        print('it is a fork')
                    if repo['language'] == 'Python':
                        print('it is in python')
                    print('')

                    fork_name = repo['full_name']
                    fork_repo_url = f"https://api.github.com/repos/{fork_name}"
                    fork_repo = requests.get(fork_repo_url,headers=headers).json()
                    orig_repo_name = fork_repo['parent']['full_name']
                    #print('\nTHE PARENT\n')
                    #print(orig_repo_name)
                    #print(fork_repo['parent'])
                    if fork_repo['parent']['private'] == False:
                        # go to 2nd page to ensure at least 200 contributors
                        orig_repo_url = f"https://api.github.com/repos/{orig_repo_name}/contributors?page=2&per_page=100"
                        orig_repo = requests.get(orig_repo_url,headers=headers).json()
                        print(len(orig_repo))
                        if len(orig_repo) == 100:
                            user_repos[user].append(orig_repo_name)
                            print(orig_repo_name)
    print(user_repos)
users = ['blink1073']
collect_data(users)
