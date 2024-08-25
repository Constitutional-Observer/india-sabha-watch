# read all txt files in dir
# parse using regex
# make into df
import os
import pandas as pd
import re

global dir
dir = "data/loksabha/txt"

def make_csv(dir):
    files = os.listdir(dir)
    df = pd.read_csv("data/loksabha/sabha-english-documentation-links.csv")

    # get file name and match text and add it to a new col called txt
    for f in files:
        filename = dir+"/"+f
        with open(filename, "r") as file:
            text = file.read()
            date = f.split('.')[0]
            df.loc[df['Date'] == date,'txt'] = text
    return df

if __name__ == "__main__":
    df = pd.read_csv("data/loksabha/sabha-english-documentation-links.csv")
    df['txt'] = ''
    df_results = make_csv(dir)

    # filter within df

    df_results.to_csv("data/loksabha/sabha-english-documentation-links-text.csv", index=False)
    print(len(df_results), " files with data")
        