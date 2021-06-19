from datetime import date
from github import Github
import os
import pandas as pd
import sys

# used on first run to set up the pickle where we'll be storing stuff


def main(my_label, pickle_file):
    go(my_label, pickle_file)
    return


def go(my_label, pickle_file):
    token = os.getenv('GITHUB_TOKEN', '...')
    g = Github(token)
    org = g.get_organization("OpenSearch-project")
    repo_list = org.get_repos()

    the_date = str(date.today())
    repo_data = []
    repo_names = []

    for repo in repo_list:
        repo_names.append(repo.name)
        repo_data.append(repo.get_issues(state="open", labels=[my_label]).totalCount)

    panda_data = {
         the_date: (repo_data)
     }

    df = pd.DataFrame(panda_data, index=repo_names)
    df.to_pickle(pickle_file)

    return


if __name__ == "__main__":
    main(str(sys.argv[1]), str(sys.argv[2]))
