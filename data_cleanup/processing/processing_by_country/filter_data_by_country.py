import pandas as pd 
from pathlib import Path

curr = Path.cwd() 
path = curr.parent.parent
#print(path) put do ociscenih podataka

file = str(path)
file+="/cleaned_data.csv"
#print(file) napravljen string pomocu kojeg cemo otvoriti cleaned_data.csv

df = pd.read_csv(file)
#print(df.info()) uspjesno procitan pdf file 

drzave = set(df["zemlja_gosta"]) 
#print(drzave) skup svih drzava gostiju
#file2 = str(curr)
#file2 += "country_data"
#print(file2)
d = list(drzave)
d.sort() #da ih imamo po abecednom redu
#f = open("country_data/countries.txt","w+")
b = ""
print(d)
for z in d:
    a = str(z)
    b += a + "\n"
#f.writelines(b)
#f.close()
