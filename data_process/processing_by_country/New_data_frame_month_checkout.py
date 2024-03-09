import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

curr = Path.cwd() 
path = curr.parent.parent
#print(path) put do ociscenih podataka

file = str(path)
file+="/cleaned_data.csv"
#print(file) napravljen string pomocu kojeg cemo otvoriti cleaned_data.csv


#razdavajamo dataset po hotelu da jasnije vidimo tendencije
df = pd.read_csv(file)
df["zemlja_gosta"] = df["zemlja_gosta"].replace("CN","CHN")
df = df[df["status_rezervacije"] == "Check-Out"]

df["datum_dolaska"] = pd.to_datetime(df["datum_dolaska"])
df["datum_odjave"] = pd.to_datetime(df["datum_odjave"])
print(df.info())

months = pd.date_range(start="2013-01",end="2018-01",freq="MS")
#mjeseci = months.tolist()

