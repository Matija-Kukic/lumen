import os, sys
import pandas as pd
parr =os.getcwd()
parr += '/obradjeni_pod/obrajdeno.parquet'
#print(parr)
df = pd.read_parquet(parr)
print(df.head())

