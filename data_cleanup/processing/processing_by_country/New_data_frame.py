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
hot1 = df[df["hotel_id"] == 0] #hotel1
hot2 = df[df["hotel_id"] == 1] #hotel2
#print(hot1.info())
#print(hot2.info())

#Obrada za hotel1
a = list(set(hot1["zemlja_gosta"]))
a.sort()
print(a)

start_date = datetime(2013, 1, 1)
end_date = datetime(2018, 1, 14)

# Define the step for the loop
step = timedelta(days=1)
d = dict()
colum = list()
colum.append("Zemlja_gosta")
# Iterate over the dates
for dt in (start_date + timedelta(n) for n in range((end_date - start_date).days + 1)):
    formatted_date = dt.strftime("%d-%m-%Y")  
    colum.append(formatted_date)
dulj = len(colum)-1
print(colum)
for z in a:
    datf = hot1[hot1["zemlja_gosta"] == z]
    dani_dolaska = []  

