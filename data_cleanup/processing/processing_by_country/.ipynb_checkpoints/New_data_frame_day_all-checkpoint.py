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
#hot1 = df[df["hotel_id"] == 0] #hotel1
#hot2 = df[df["hotel_id"] == 1] #hotel2
#print(hot1.info())
#print(hot2.info())

#Obrada za hotel
a = list(set(df["zemlja_gosta"]))
a.sort()
print(a)

start_date = datetime(2013, 1, 1)
end_date = datetime(2018, 1, 14)

# Define the step for the loop
step = timedelta(days=1)
d = dict()
colum = list()
colum.append("Zemlja_gosta")
colum.append("Ukupno")
# Iterate over the dates
for dt in (start_date + timedelta(n) for n in range((end_date - start_date).days + 1)):
    formatted_date = dt.strftime("%Y-%m-%d")  
    colum.append(formatted_date)
dulj = len(colum)-1
#print(colum)
new_df = pd.DataFrame(columns = colum)
print(new_df.info())
#print(colum)
for z in a:
    datf = df[df["zemlja_gosta"] == z]
    new_row = []  
    new_row.append(z)
    dolasci = list(datf["datum_dolaska"])
    odlasci = list(datf["datum_odjave"])
    #print(z) 
    #print(dolasci)
    #print(odlasci)
    ukupno = 0
    start_date = datetime(2013, 1, 1)
    end_date = datetime(2018, 1, 14)
    d = dict()
    d["zemlja_gosta"] = z
    d["Ukupno"] = 0
    # Define the step for the loop
    step = timedelta(days=1)
    # Iterate over the dates
    for dt in (start_date + timedelta(n) for n in range((end_date - start_date).days + 1)):
        formatted_date = dt.strftime("%Y-%m-%d")  
        d[formatted_date] = 0
   
    for i in range(len(dolasci)):
        sd = datetime.strptime(dolasci[i],"%Y-%m-%d") 
        ed = datetime.strptime(odlasci[i],"%Y-%m-%d")
        #print(sd)
        step = timedelta(days=1)
        for j in range((ed-sd).days + 1):
            d[sd.strftime("%Y-%m-%d")] += 1
            sd = sd + timedelta(days=1)
            ukupno+=1
    d["Ukupno"] = ukupno
    dani = list(d.values()) 
    #if z == "PRT":
    #    print(dani)
    new_df = new_df._append(pd.Series(dani,index=new_df.columns),ignore_index=True)
print(new_df.info())
new_df.to_csv("country_data/no_of_reservations_per_country.csv")
