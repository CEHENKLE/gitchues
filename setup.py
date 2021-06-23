from datetime import date
from github import Github
import os
import pandas as pd
import sys


# used on first run to set up the pickle where we'll be storing stuff
def main(labels, my_org):
    token = os.getenv('GITHUB_TOKEN', '...')
    g = Github(token)
    org = g.get_organization(my_org)

    repo_data = []
    repo_names = []
    panda_list = []

    for repo in org.get_repos():
        repo_names.append(repo.name)
    the_date = str(date.today())

# I bet there's a more pythonic way to do this.
    for label in labels:
        for repo in org.get_repos():
            repo_data.append(repo.get_issues(state="open", labels=[label]).totalCount)
        panda_list.append({
             the_date: (repo_data)
             })
        repo_data = []
# see, this I like ;)
    dataframes = list(map(lambda x: pd.DataFrame(x, index=repo_names), panda_list))
    print(dataframes)
    i = 0
    for dataframe in dataframes:
        dataframe.to_pickle("gitchues-"+labels[i]+".pkl")
        i += 1
    return


if __name__ == "__main__":
    main(list(sys.argv[1]), str(sys.argv[2]))
