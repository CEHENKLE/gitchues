from datetime import date
import pandas as pd
from github import Github
import os
from pathlib import Path
import setup
import report

# Resources I found helpful:
# Panda
# Tutorial: https://www.tutorialspoint.com/python_pandas/python_pandas_dataframe.htm
# Plotting Pandas https://datatofish.com/plot-dataframe-pandas/
# https://www.geeksforgeeks.org/adding-new-column-to-existing-dataframe-in-pandas/
# https://www.c-sharpcorner.com/article/add-assign-and-modify-values-in-dataframe/

#get a ticket we can use that we've set in our system variables.
token = os.getenv('GITHUB_TOKEN', '...')
g = Github(token)

#overwrite this to whatever org you care about

my_org = "OpenSearch-project"
org = g.get_organization(my_org)

#I always assume you want to find "Open" issues plus one of these labels.
labels = ["untriaged", "v1.0.0"]
picklefiles = []
dataframes = []

for label in labels:
    picklefiles.append(Path("./gitchues-"+label+".pkl"))

# Get a list of orgs and today's date
repo_list = org.get_repos()
the_date = str(date.today())

#Check and see if this is the first run by seeing if our Pickle file is there.  If it's not, we need to build one.

if not all(os.path.exists(file) for file in picklefiles):
    setup.main(labels, my_org)

# get your source data, unpickle it.
for file in picklefiles:
    dataframes.append(pd.read_pickle(file))

#add new new column with today's date,insert data into the new column using the repo name as the index.  This will overwrite existing data is we run it again on the day. I am okay with this.

for dataframe, label in zip(dataframes, labels):
    for repo in repo_list:
        if repo.name in dataframe.index:
             dataframe.loc[repo.name, the_date] = repo.get_issues(state="open", labels=[label]).totalCount
        else:
             #the first time this happens, I'll go back and add a new row with 0s and then update.  But for now, whistling past the graveyard.
            print("Houston, we have a problem")


# Generate report
report.main(dataframes, labels)

#pickle back out
j = 0
for dataframe in dataframes:
    dataframe.to_pickle("gitchues-"+labels[j]+".pkl")
