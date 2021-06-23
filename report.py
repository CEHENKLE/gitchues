from datetime import date

# Used to print pretty reports.  Will get prettier
def main(dataframes, labels):
    the_date = str(date.today())
    for dataframe, label in zip(dataframes, labels):
        print(dataframe)
        file_name = "Github-" + label + "-new-" + the_date + "-issues.csv"
        dataframe.to_csv(file_name)
    return
