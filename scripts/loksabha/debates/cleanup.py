import bs4 as soup
import random
import ast 
import shortuuid
import pandas as pd
# open a random html

def cleanupTable(s):
    # remove "\xa0"
    s = s.replace("\\xa0", " ")
    return s

def cleanupKeys(s):
    # remove colens 
    s = {k.replace(": ", " ").strip().replace(" ", "_"): v for  k,v in s.items()}
    print(s)
    return s

def splitCapital(s):
    # read words
    # if word contains two capital letters, split and insert a comma
    texts = s.split(' ')
    for i,t in enumerate(texts):
        for c in t:
            if c.isupper() and t.index(c) != 0:
                # push into a position inbetween in the arry
                temp = t[:t.index(c)] + ", " + t[t.index(c):]
                texts[i] = temp
    return " ".join(texts)

df = pd.read_csv("data/loksabha/sabha-debates-individual-documentation-links-joined.csv")
df.dropna(subset="Meta", inplace=True)

df["Meta"] = df["Meta"].apply(lambda x: cleanupTable(x))

df["Meta"] = df["Meta"].apply(lambda x: ast.literal_eval(x))

df["Meta"] = df["Meta"].apply(lambda x: cleanupKeys(x))


# get keys in the dictionary
df["Participants"] = df["Meta"].apply(lambda x: splitCapital(x['Members'] if "Members" in x.keys() else ""))
df["Lok_Sabha_Number"] = df["Meta"].apply(lambda x: x["Lok_Sabha_Number"] if "Lok_Sabha_Number" in x.keys() else "")
df['Session_Number'] = df["Meta"].apply(lambda x: x["Session_Number"] if "Session_Number" in x.keys() else "")
df.rename(columns={"Category": "Type"}, inplace=True)
df['Type'] = df["Meta"].apply(lambda x: x["Debate"] if "Debate" in x.keys() else "")

# keep only unique indixes
df.drop_duplicates(subset=["Index"], keep="first", inplace=True)


# parse as date 
df["Date"] = df["Date"].apply(lambda x: pd.to_datetime(x))

df.sort_values("Date", inplace=True, ascending=False)

# create new index 
df.reset_index(inplace=True, drop=True)
df['Index'] = df.index
# set index of df

df.drop(columns=["Meta"], inplace=True)

df.drop(columns="Index")

# apply uuid to every row
df["UUID"] = ''
df['UUID'] = df["UUID"].apply(lambda x: shortuuid.uuid())

df.to_csv("data/loksabha/sabha-debates-individual-documentation-flattened-1.csv", index=False)
