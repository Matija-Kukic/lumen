import pandas as pd
import numpy as np
dataset_path = 'lumen_dataset/data/lumen/export_df.parquet'
df = pd.read_parquet(dataset_path)
#print(df.head())
#df.info()
#df.describe()
a = list((df['datum_odjave']-df['datum_dolaska'])/np.timedelta64(1,'D'))
for i in range(len(a)):
    if a[i] == 0:
        a[i] = 1
df['broj_nocenja'] = a
df['ukupno_placeno'] = df['broj_nocenja'] * df['cijena_nocenja']
#print(a)
#print(df.head())
#f = open("data_u_txt.txt","w+")
#f.write(df.head().to_string())
#f.close()
#df.to_parquet('obradjeni_pod/obrajdeno.parquet')
#df.to_csv('obradjeni_pod/obradjeno_csv.csv')