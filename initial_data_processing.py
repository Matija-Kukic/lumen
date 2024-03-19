import pandas as pd
import numpy as np
dataset_path = "lumen_dataset/data/lumen/export_df.parquet"
train_dataset = "lumen_dataset/data/lumen/train.parquet"
df = pd.read_parquet(dataset_path)
train_df = pd.read_parquet(train_dataset)
train_df["date_from"] = pd.to_datetime(train_df["date_from"])
train_df["reservation_date"] = pd.to_datetime(train_df["reservation_date"])
train_df["date_to"] = pd.to_datetime(train_df["date_to"])
train_df["stay_date"] = pd.to_datetime(train_df["stay_date"])
train_df["cancel_date"] = pd.to_datetime(train_df["cancel_date"])
#print(df.head())
#df.info()
#df.describe()
a = list((df["datum_odjave"]-df["datum_dolaska"])/np.timedelta64(1,"D"))
b = list((train_df["date_to"]-train_df["date_from"])/np.timedelta64(1,"D"))
for i in range(len(a)):
    if a[i] == 0:
        a[i] = 1
df["broj_nocenja"] = a
df["ukupno_placeno"] = df["broj_nocenja"] * df["cijena_nocenja"]
del train_df["night_number"]
for i in range(len(b)):
    if b[i] == 0:
        b[i] = 1
train_df["stay_nights"] = b
train_df["price_per_night"] = train_df["price"] / train_df["stay_nights"]
#f = open("data_u_txt.txt","w+")
#f.write(df.head().to_string())
#f.close()
df.to_parquet("data_process/processed.parquet")
df.to_csv("data_process/processed_csv.csv")
train_df.to_parquet("data_process/train_processed.parquet")
train_df.to_csv("data_process/train_processed.csv")