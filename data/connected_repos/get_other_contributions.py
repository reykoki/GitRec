import pandas as pd
import requests
from github import Github
import pickle

with open('access_token.txt') as f:
    contents = f.read()
    access_token = contents.split('\n', 1)[0]
headers = {'Authorization':"Token "+access_token} # we need header to obtain more data

user_repo_data = {}

def collect_data(usernames):
    # set up user name we want to research and get your own access_token , then create header
    for user in usernames:
        user_repos = [] 
        entry_per_page = 100
        pg_num = 1
        all_repos = []
        while entry_per_page > 0:
            url = f"https://api.github.com/users/blink1073/repos?page={pg_num}&per_page=100"
            repos = requests.get(url,headers=headers).json()
            pg_num += 1
            entry_per_page = len(repos)
            for repo in repos:

                if repo['private'] == False and repo['fork'] == True and repo['language'] == 'Python':
                    fork_name = repo['full_name']
                    fork_repo_url = f"https://api.github.com/repos/{fork_name}"
                    fork_repo = requests.get(fork_repo_url,headers=headers).json()
                    orig_repo_name = fork_repo['parent']['full_name']
                    if fork_repo['parent']['private'] == False:
                        # go to 2nd page to ensure at least 200 contributors
                        orig_repo_url = f"https://api.github.com/repos/{orig_repo_name}/contributors?page=2&per_page=100"
                        orig_repo = requests.get(orig_repo_url,headers=headers).json()
                        if len(orig_repo) == 100:
                            user_repos.append(orig_repo_name)
        if len(user_repos) > 0:
            user_repo_data[user] = user_repos

    return user_repo_data


                            
users = ['blink1073', 'OBITORASU']
users = pickle.load(open(r"../repo_contributors/all_sig_names.pickle","rb"))

user_repo_data = collect_data(users)
#print(user_repo_data)

pickle.dump(user_repo_data, open('user_contributions.pickle', 'wb'))
