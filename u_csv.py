import pandas as pd
import numpy as np
dataset_path = 'lumen_dataset/data/lumen/export_df.parquet'
df = pd.read_parquet(dataset_path)
df.to_csv('obradjeni_pod/data_u_csvu.csv')
a = list(df['broj_djece_gostiju'])
print(a)
print(max(a))