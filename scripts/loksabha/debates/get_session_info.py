import pandas as pd

link = "https://sansad.in/api_ls/business/AllLoksabhaAndSessionDates"

df = pd.read_json(link)
#explode the df
df = df.explode("sessions")
print(df)
