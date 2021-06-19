from datetime import date
import pandas as pd
from github import Github
from shutil import copyfile
import os
from pathlib import Path
from setup import go

# Resources I found helpful:
# Panda
# Tutorial: https://www.tutorialspoint.com/python_pandas/python_pandas_dataframe.htm
# Plotting Pandas https://datatofish.com/plot-dataframe-pandas/
# https://www.geeksforgeeks.org/adding-new-column-to-existing-dataframe-in-pandas/
# https://www.c-sharpcorner.com/article/add-assign-and-modify-values-in-dataframe/


#get a ticket we can use that we've set in our system variables.
token = os.getenv('GITHUB_TOKEN', '...')
g = Github(token)

#overwrite this to whatever org you care about, and whatever you want to call your storage file. and the label you want to check for
#I want to support multiple labels.  Will refactor to do so.
org = g.get_organization("OpenSearch-project")
label1 = "untriaged"
#label2 = "v1.0.0"
picklefile1 = Path("./"+label1+"-test.pkl")
#picklefile2 = Path("./"+label2+"-test.pkl")

# Get a list of orgs and today's date
repo_list = org.get_repos()
the_date = str(date.today())

#Check and see if this is the first run by seeing if our Pickle file is there.  If it's not, we need to build one.
#again, messy.  I am dissapoint, Charlotte.
if not picklefile1.exists():
    go(label1, picklefile1)
 #   go(label2, picklefile2)

# let's back those pickles up.
copyfile("issue-tracker-untriaged.pkl", label1+the_date+".pkl")
#copyfile("issue-tracker-untriaged.pkl", label2+the_date+".pkl")

# get your source data
unpickled_untriaged = pd.read_pickle(picklefile1)
#unpickled_ga = pd.read_pickle("./issue-tracker-ga.pkl")

#add new new column with today's date,insert data into the new column using the repo name as the index.  This will overwrite existing data is we run it again on the day. I am okay with this.

for repo in repo_list:
    if repo.name in unpickled_untriaged.index:
        unpickled_untriaged.loc[repo.name,the_date] = repo.get_issues(state="open", labels=[label1]).totalCount
    else:
        #the first time this happens, I'll go back and add a new row with 0s and then update.  But for now, whistling past the graveyard.
        print("Houston, we have a problem")


#We have the index from the DF. We have data in the repos. We just need to figure out how to build a dict or list in the same order as our existing DF.

# Generate report
file_name = "Github-"+label1+"-"+the_date+"-issues.csv"
unpickled_untriaged.to_csv(file_name)

#pickle back out
unpickled_untriaged.to_pickle(picklefile1)
