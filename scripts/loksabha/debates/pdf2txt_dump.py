import os
import pandas as pd
import requests
from pandarallel import pandarallel

pandarallel.initialize(progress_bar=True)

def download_pdfs(dir, filename, link):
    filename = dir+"/"+filename+".pdf"
    if not os.path.isfile(filename):
        try: 
            file = requests.get("https://eparlib.nic.in/"+link).content
            with open(filename, "wb") as f:
                f.write(file)
            print(filename, " downloaded")
        except:
            print(filename, " failed")
    else:
        print(filename, " exists")

def dump_txt(dir):
    createTxt = "cd data/pdf_bkup; for f in *.pdf; do pdftotext $f $f.txt; done"
    os.system(createTxt)

if __name__ == "__main__":
    fdir = "data/pdf_bkup"
    df = pd.read_csv("data/loksabha/sabha-english-documentation-links.csv")
    df = df.sample(1000)
    df.parallel_apply(lambda x: download_pdfs(fdir, x["UUID"], x["PDF_Link"]), axis=1)
    dump_txt(fdir)