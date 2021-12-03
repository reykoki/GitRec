import pandas as pd
import requests
from github import Github
import pickle

access_token='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'
headers = {'Authorization':"Token "+access_token} # we need header to obtain more data

def collect_data(repo_name_list):
    # set up user name we want to research and get your own access_token , then create header
    for repo_name in repo_name_list:
        num_ppl_per_page = 100
        pg_num = 1
        all_contributors=[]
        # github is dumb and won't let you load more than 100 items per page
        while num_ppl_per_page > 0:
            url = f"https://api.github.com/repos/{repo_name}/contributors?page={pg_num}&per_page=100&anon=true"
            pg_num += 1
            contributors = requests.get(url,headers=headers).json()
            num_ppl_per_page = len(contributors)
            all_contributors.append(contributors)

        #pickle.dump(all_contributors, open('all_contributors.pickle', 'wb'))
        #all_contributors = pickle.load(open("all_contributors","rb"))

        # collect contributors names and their contribution count
        names=[]
        counts=[]
        # significant contributors (more than 5)
        sig_names = []
        num_pages = len(all_contributors)
        for page_num in range(num_pages):
            for contributor in all_contributors[page_num]:
                try:
                    name=contributor['login']
                    count=contributor['contributions']
                    names.append(name)
                    counts.append(count)
                    if count > 5:
                        sig_names.append(name)
                except:
                    name=contributor['name']
                    count=contributor['contributions']
                    names.append(name)
                    counts.append(count)


        names_file = open("name_file.txt", "a")
        for element in set(sig_names):
            names_file.write(element + "\n")
        names_file.close()

        # create a dataframe and store the contrbutors' names and their contribution counts
        mydata=pd.DataFrame()
        mydata['contributor_name']=names
        mydata['counts']=counts

        # Then obtain unique names with sum of their contribution counts
        mydata=mydata.groupby('contributor_name')["counts"].sum().reset_index().sort_values(by='counts',ascending=False)
        # drop None / missing values
        mydata=mydata.dropna(axis=0).reset_index().drop(columns='index')
        # save mydata
        #mydata.to_csv("contributor_data/" + repo_name + "_contributors.csv")

repo_name = ['gvalkov/python-evdev',
             'pypa/pip',
             #'pandas-dev/pandas',
             #'tensorflow/tensorflow',
             #'scikit-learn/scikit-learn',
             #'nilearn/nilearn',
             #'Theano/Theano',
             #'matplotlib/matplotlib',
             #'keras-team/keras',
             #'opencv/opencv',
             #'pytorch/pytorch',
             ]
collect_data(repo_name)
