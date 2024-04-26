import numpy as np
import math
import statistics
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
from scipy.stats import boxcox
from scipy.stats import shapiro 
from scipy.stats import lognorm
from scipy.stats import kstest,norm
from scipy.stats import lognorm
from pmdarima import auto_arima
import warnings
warnings.filterwarnings("ignore")


def process(path):
    train_df = pd.read_parquet(path)
    train_df["date_from"] = pd.to_datetime(train_df["date_from"])
    train_df["reservation_date"] = pd.to_datetime(train_df["reservation_date"])
    train_df["date_to"] = pd.to_datetime(train_df["date_to"])
    train_df["stay_date"] = pd.to_datetime(train_df["stay_date"])
    train_df["cancel_date"] = pd.to_datetime(train_df["cancel_date"])
    #print(df.head())
    #df.info()
    #df.describe()
    b = list((train_df["date_to"]-train_df["date_from"])/np.timedelta64(1,"D"))
    del train_df["night_number"]
    for i in range(len(b)):
        if b[i] == 0:
            b[i] = 1
    train_df["stay_nights"] = b
    train_df["price_per_night"] = train_df["price"] / train_df["stay_nights"]
    #f = open("data_u_txt.txt","w+")
    #f.write(df.head().to_string())
    #f.close()

    return train_df

def cleaning(data1):
    df = data1
    df = df[df["date_from"] >= df["reservation_date"]]
    df = df[ (df["reservation_date"] <= df["cancel_date"] ) | (df["cancel_date"].isna())]
    df = df[df["adult_cnt"] > 0]
    df = df[ (df["cancel_date"] < df["date_to"]) | (df["cancel_date"].isna())  ]
    df.drop_duplicates(subset = "reservation_id", inplace = True, keep = "first")
    df = df[df["reservation_status"] == "Checked-out"]
    df["guest_count"] = df["adult_cnt"] + df["children_cnt"]
    df["nightly_price_per_guest"] = df["price_per_night"] / df["adult_cnt"]
    prices_df = df[df["price_per_night"] > 150]
    prices_df = prices_df[prices_df["nightly_price_per_guest"] < 6500]
    #prices_df.to_parquet("train_data_cleaned.parquet") 
    return prices_df
def model(df):
    room_occupancy = df[(df["cancel_date"].isna())]
    
    dates = []
    for index, row in room_occupancy.iterrows():
        delta = (row["date_to"] - row["date_from"]).days
        for i in range(delta):
            dates.append((row["date_from"] + pd.Timedelta(days=i), row["room_cnt"]))
    
    
    room_dates_df = pd.DataFrame(dates, columns=["date", "room_cnt"])
    
    
    room_occupancy = room_dates_df.groupby("date")["room_cnt"].sum().reset_index()
    room_occupancy.index = room_occupancy["date"]
    del room_occupancy["date"]

    room_occupancy["room_count_log"] = np.log(room_occupancy["room_cnt"])
    
    seasonal_difference = room_occupancy['room_count_log'].diff(periods=365)
    
    seasonal_difference = seasonal_difference.dropna()
    seasonal_difference_df = seasonal_difference.to_frame(name='room_cnt').reset_index()
    seasonal_difference_df.columns = ['date', 'room_cnt']  
    seasonal_difference_df = seasonal_difference_df[seasonal_difference_df["date"] > "2009-01-01"]

    test = room_occupancy.iloc[2:368]
    train = room_occupancy.iloc[368:-1]
    
    model = auto_arima(seasonal_difference_df["room_cnt"], seasonal = True, trace = False, approx = False, m = 7)
    order_tuple = tuple(model.order)
    seasonal_order_tuple = tuple(model.seasonal_order)

    mod = ARIMA(seasonal_difference_df["room_cnt"], order = order_tuple, seasonal_order = seasonal_order_tuple)
    mod = mod.fit()

    start = len(seasonal_difference_df)
    end = len(test) + len(seasonal_difference_df) - 1
    
    pred = mod.predict(start = start, end = end)
    
    original_train = room_occupancy.iloc[369:]
    print(len(pred), len(test))
    prediction_list = list()
    for i, data in enumerate(train["room_count_log"]):
        prediction_list.append(data)
    for i, prediction in enumerate(pred):
        prediction_list[i] += prediction
    for i in range(len(prediction_list)):
        prediction_list[i] = math.exp(prediction_list[i])
    print(prediction_list)
    # Now, 'reverted_values' contains the predicted values in their original scale
    residuals = test["room_cnt"] - prediction_list
    residuals_list = residuals.values.tolist()
    abs_residuals_list = list(map(abs, residuals_list))
    abs_residuals_list = sorted(abs_residuals_list)
    alpha_quantile = np.quantile(abs_residuals_list, 1 - 0.20 / 2)
    residuals_list = residuals.values.tolist()
    residuals_sorted = np.sort(residuals_list)
    
    p_values = [(np.sum(residuals_list >= r) + 1) / (len(residuals_list) + 1) for r in residuals_sorted]
    alpha = 0.05
    
    upper_quantile = np.quantile(residuals_sorted, 1 - alpha / 2)
    lower_quantile = np.quantile(residuals_sorted, alpha / 2)
    
    def predict_new_point(prediction_point):
        upper_bound = prediction_point + upper_quantile
        lower_bound = prediction_point + lower_quantile
        return lower_bound, upper_bound
    
    lower_list = list()
    upper_list = list()
    for i in prediction_list:
        lo, hi = predict_new_point(i)
        lower_list.append(lo)
        upper_list.append(hi)
    date_list = test.index.tolist()
    plt.figure(figsize=(50, 10))
    plt.plot(date_list, prediction_list,color = "red")
    plt.plot(date_list, upper_list,color = "orange")
    plt.plot(date_list, lower_list,color = "orange")
    plt.plot(test.index, test["room_cnt"], color="blue")
    plt.fill_between(date_list, upper_list, lower_list, color='gray', alpha=0.3)
    
    plt.title("Ukupan broj zauzetih soba")
    plt.xlabel("Datum")
    plt.ylabel("Ukupan broj gostiju")
    plt.xticks(rotation = 45) 
    plt.tight_layout()  
    plt.show()
def main():
    path = Path.cwd().parent.parent
    path = str(path)
    path += "/lumen_dataset/data/lumen/train.parquet" 
    data1 = process(path) 
    data2 = cleaning(data1)
    model(data2) 
if __name__ == "__main__":
    main()