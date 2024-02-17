import pandas as pd 
from pathlib import Path

curr = Path.cwd() 
path = curr.parent.parent
#print(path) uspjesno dohvacen put do ociscenih podataka

file = str(path)
file+="/cleaned_data.csv"
#print(file) napravljen string pomocu kojeg cemo otvoriti cleaned_data.csv

df = pd.read_csv(file)
print(df.info())


