# read all txt files in dir
# parse using regex
# make into df
import os
import pandas as pd
import re

dir = "data/pdf_bkup"

def extract_text(files):
    df_results = pd.DataFrame()
    for f in files:
        if f.endswith(".txt"):
            with open(os.path.join(dir, f), 'r', encoding="utf8") as myfile:
                pd.set_option("display.max_colwidth", 1000)
                data = myfile.read()
                
                # insert \n------ at the end of the file
                data = data + "\n------"

                # title is the first line of data
                title = re.findall(r"(.*)(?=\n(?:SHRI|KUMARI|माननीय अध्यक्ष|श्री|SHRIMATHI|डॉ.|DR.|HON\.|\\z))",data)
                reg = r"(SHRI|HRI|SARDAR|श्री|DR.|Mr.|KUNWAR|कुँवर|डॉ.|शी|थी|PROF.|KUMARI|माननीय|मती|ADV.|SECRETARY|SHRIMATHI|रीमती|HON\.)([^:]*)(:)(.*?)(?=\n(?:SHRI|KUMARI|Mr.|रीमती|थी|HRI|शी|SARDAR|माननीय अध्यक्ष|PROF.|ADV.|SECRETARY|KUNWAR|कुँवर|श्री|SHRIMATHI|श्रीमती|डॉ.|DR.|------|HON\.|\\z))"
                result = re.findall(reg, data, flags=re.DOTALL|re.MULTILINE)

                # parse the result 
                # make into a obj structure
                # {speaker: "", dialogue: ""}
                formattedResult = []

                
                if len(result) == 0:
                    result = None
                    print(f, "has no data")
                else:
                    for i in result:
                        speaker = i[1]
                        dialogue = i[3]
                        formattedResult.append({"Speaker": speaker, "Dialogue": dialogue})
                if len(title) == 0:
                    pass
                    # dont truncate text when printing on terminal
                    # print(f, "has no title")
                    # search for titile in df
                    # print(df[df["UUID"] == f.split(".")[0]]['Title'])

                df_results = df_results._append({"UUID": f.split(".")[0], "Title": title, "Text": formattedResult}, ignore_index=True)
    return df_results

if __name__ == "__main__":
    files = os.listdir(dir)
    df = pd.read_csv("data/loksabha/sabha-debates-individual-documentation-flattened.csv")

    df_results = extract_text(files)
    print(len(files)/2, " files")
    
    # filter within df
    df_results.rename(columns={"Title": "Title_PDF"}, inplace=True)
    df = df.join(df_results.set_index("UUID"), on="UUID")
    df.dropna(subset="Text", inplace=True)
    df.to_csv("data/loksabha/sabha-debates-individual-documentation-flattened-extracted.csv", index=False)
    print(len(df_results), " files with data")
        