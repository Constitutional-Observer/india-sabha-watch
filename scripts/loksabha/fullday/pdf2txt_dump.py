import os
import pandas as pd
import requests
from pandarallel import pandarallel

pandarallel.initialize(progress_bar=True)

def download_pdfs(dir, filename, link):
    filename = dir+"/"+filename+".pdf"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    if not os.path.isfile(filename):
        try: 
            file = requests.get("https://eparlib.nic.in/"+link, headers=headers).content
            with open(filename, "wb") as f:
                f.write(file)
            print(filename, " downloaded")
        except Exception as e:
            print(e)
            print(filename, " failed")
    else:
        print(filename, " exists")

def dump_txt(dir):
    createTxt = "cd data/pdf_bkup; for f in *.pdf; do pdftotext $f $f.txt; done"
    os.system(createTxt)

if __name__ == "__main__":
    fdir = "data/pdf_bkup/day"
    df = pd.read_csv("data/loksabha/sabha-english-documentation-links.csv")
    df.apply(lambda x: download_pdfs(fdir, x["Date"], x["PDF_Link"]), axis=1)
    dump_txt(fdir)