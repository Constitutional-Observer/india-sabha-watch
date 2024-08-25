import pandas as pd
import bs4 as soup
import requests
from io import StringIO
from tqdm import tqdm
import time

from concurrent.futures import ThreadPoolExecutor

Englishlink = "https://eparlib.nic.in/simple-search?page-token=63dbc7fa77d0&page-token-value=a982e808be30077f19f95caabd94f345&location=123456789%2F2963706&query=&rpp=2500&sort_by=dc.date_dt&order=desc&filter_field_1=loksabhanumber&filter_type_1=equals&filter_value_1=17&submit_filter_remove_1=X"

OriginalLink = "https://eparlib.nic.in/handle/123456789/7/simple-search?query=&filter_field_1=title&filter_type_1=equals&filter_value_1=Lok+Sabha+Debates&sort_by=dc.date_dt&order=desc&rpp=7000&etal=0&start=20"


def download_all_parent_html(link):
    for i in range(99740, 129136, 20):
        tlink = link + str(i)
        # tempdf = get_full_table(tlink)
        # download all html Files

        file = requests.get(tlink).content

        with open("../data/sabha/htmlbkup/part2/" + str(i) + ".html", "wb") as f:
            f.write(file)

        ## sleep randomly between 1 and 2 seconds
        time.sleep(random.randint(1, 5))

def download_all_meta_html(df):
    for i, x in enumerate(tqdm(df["Meta_Link"])):
        print(x)
        file = requests.get(x).content
        with open("../data/sabha/htmlbkup/part2/meta/" + str() + ".html", "wb") as f:
            f.write(file)
        time.sleep(random.randint(1, 3))

def get_full_table(html):
    # get the table which is some child to "discovery-result-results"
    # and construct a pd df
    # html = requests.get(link).content
    content = soup.BeautifulSoup(html, "html.parser")

    # get the links in the table as well instead of the text

    table = content.find("table")
    df = pd.read_html(StringIO(str(table)), extract_links="body")[0] 

    print(df)
    df["Date"] = df["Date"].apply(lambda x: x[0])
    df["View"] = df["View"].apply(lambda x: x[1])
    df["Title"] = df["Title"].apply(lambda x: x[0])
    df['Type'] = df['Type'].apply(lambda x: x[0])
    df['Members'] = df['Members'].apply(lambda x: x[0])

    #rename link
    df.rename(columns={"View": "Meta_Link"}, inplace=True)

    # append this before the link
    pre = "https://eparlib.nic.in/"
    df["Meta_Link"] = pre + df["Meta_Link"]

    return df

# Open each link and find link with class btn-primary. get href

def get_pdf_meta_link(html):
    try:
        body = soup.BeautifulSoup(html, "html.parser")

        # get file name in table under parent div with class panel-info
        table = body.select_one("div.panel-info table td[headers=t1] a")
        link = table["href"]
        name = table.text 

        # get metadata in table with class itemDisplayTable
        table = body.select("table.itemDisplayTable tr")
        metatable = {i.select_one("td.metadataFieldLabel").text:
                    i.select_one("td.metadataFieldValue").text for i in table}
        return name, link, metatable

    except Exception:
        return ("", "", {})

def read_html_extract_tables(dir):
    dfParent = pd.read_csv("../data/sabha-debates-individual-documentation-links-meta.csv")
    df = pd.DataFrame(columns=["PDF_Name", "PDF_Link", "Meta", "Index"])

    # create a new csv file
    # df.to_csv("../data/sabha-debates-individual-documentation-links-meta.csv", mode="w", index=False)
    
    # make a new list of files
    # that dont exist in the df
    listFiles = os.listdir(dir)
    # if file in dfParent dont, remove
    listFiles = [x for x in listFiles if int(x.split(".")[0]) not in dfParent["Index"].values] 
    print(len(listFiles))   

    # read all files from dir
    for i, file in enumerate(listFiles):
        if file.endswith(".html"):
            path = os.path.join(dir, file)

            # check if file.strip(".")[0] is in index in df
            # if not, append
            # if yes, skip

            # get html content
            html = open(path, "r").read()
            
            # read html
            PDF_Name, PDF_Link, Meta = get_pdf_meta_link(html)

            # append to dataframe
            df = df._append({"PDF_Name": PDF_Name, "PDF_Link": PDF_Link, "Meta": Meta, "Index": file.split(".")[0]}, ignore_index=True)

            
            if i % 1000 == 0 and i != 0:
                print(i)
                # append to csv
                df.to_csv("../data/sabha-debates-individual-documentation-links-meta.csv", mode="a", index=False, header=False)
                df = pd.DataFrame(columns=["PDF_Name", "PDF_Link", "Meta", "Index"])

    return df

def get_parent_tables(link):
    download_all_parent_html(link)
    df = read_html_extract_tables("../data/sabha/htmlbkup/part2")
    return df

def get_meta_tables(df):
    df.apply(lambda x: download_all_meta_html(x))
    df = read_html_extract_tables("../data/sabha/htmlbkup/part2/meta")

if __name__ == "__main__":
    df = get_parent_tables(OriginalLink)
    metadf = get_meta_tables(df)

    # merge the two
    df = df.merge(metadf, on="Index")
    df.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis=1, inplace=True)
    # set index of df

    df.to_csv("data/sabha-debates-individual-documentation-links-joined.csv", index=False)