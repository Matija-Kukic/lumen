import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib as jl
from datetime import datetime
from pathlib import Path
import math

def prediction(df):
    model = jl.load('arima_trained.pkl')
    #df = pd.read_parquet('test.parquet')
     
    df.drop_duplicates(subset = "reservation_id", inplace = True, keep = "first")
    
    room_occupancy = df[(df["cancel_date"].isna())]
    dates = []
    for index, row in room_occupancy.iterrows():
        delta = (row["date_to"] - row["date_from"]).days
        for i in range(delta):
            dates.append((row["date_from"] + pd.Timedelta(days=i), row["room_cnt"]))

    room_dates_df = pd.DataFrame(dates, columns=["date", "room_cnt"])
    room_occupancy = room_dates_df.groupby("date")["room_cnt"].sum().reset_index() 
    room_occupancy.index = room_occupancy["date"]
    date_list = room_occupancy.index.tolist()
    del room_occupancy["date"]
    #room_occupancy.head()
    df['date_from'] = pd.to_datetime(df['date_from'])
    df['date_to'] = pd.to_datetime(df['date_to'])
    date1 = df["date_from"].min()
    date2 = df["date_to"].max()
    start = (date1 - datetime(2010,1,2)).days
    end = int((date2-date1).days) + start
    #print(start,end,date1,date2)
    pred = model.predict(start+366,end+366)
    #print(pred)

    #path = Path.cwd().parent
    #filePath = str(path) + "data_cleanup/second_dataset/train_data_price_corrected.parquet"
    #df2 = pd.read_parquet(filePath)

    '''
    path = Path.cwd()
    print("path je: ", path)
    filePath = str(path) + "/backend/train_data_price_corrected.parquet"
    print("filePath je: ", filePath)
    '''

    # Get the path to the Parquet file
    file_path = Path(__file__).parent / "train_data_price_corrected.parquet"

    # Convert the Path object to a string
    filePath = str(file_path)

    df2 = pd.read_parquet(filePath)
    room_occupancy2 = df2[(df2["cancel_date"].isna())]
    
    dates2 = []
    for index, row in room_occupancy2.iterrows():
        delta = (row["date_to"] - row["date_from"]).days
        for i in range(delta):
            dates2.append((row["date_from"] + pd.Timedelta(days=i), row["room_cnt"]))

    room_dates_df2 = pd.DataFrame(dates2, columns=["date", "room_cnt"])

    room_occupancy2 = room_dates_df2.groupby("date")["room_cnt"].sum().reset_index()
    room_occupancy2.index = room_occupancy2["date"]
    del room_occupancy2["date"]
    room_occupancy2["room_count_log"] = np.log(room_occupancy2["room_cnt"])
    test = room_occupancy2.iloc[2:368]
    train = room_occupancy2.iloc[368:-1]
    test_list =  test["room_cnt"].tolist()
    train_list = train["room_cnt"].tolist()
    mid_point_test = list()
    for i in range(end-start):
        mid_point_test.append((test_list[i] + train_list[i]) / 2)
    prediction_list = list()
    for i, data in enumerate(train["room_count_log"]):
        if i >= start and i <= end:
            prediction_list.append(data)
        else:
            continue
    print(len(prediction_list))
    for i, prediction in enumerate(pred):
        prediction_list[i] += prediction
    for i in range(len(prediction_list)):
        prediction_list[i] = math.exp(prediction_list[i])

    residuals = list()
    residuals_list = residuals

    for i in range(len(mid_point_test)):
        residuals.append(mid_point_test[i]-prediction_list[i])
    residuals_sorted = np.sort(residuals_list)
   
    #REAL SCIENCES USE 5 SIGMA FOR P VALUE, WE ARE NOT REAL SCIENTISTS BUT PSYCOLOGYSTS STILL TAKE THEMSEVLES SERIOUSLY 
    #SO CAN WE!!!!!!!!
    p_values = [(np.sum(residuals_list >= r) + 1) / (len(residuals_list) + 1) for r in residuals_sorted]
    alpha = 0.05
    
    upper_quantile = np.quantile(residuals_sorted, 1 - alpha / 2)
    lower_quantile = np.quantile(residuals_sorted, alpha / 2)
    
    def predict_new_point(prediction_point):
        upper_bound = prediction_point + upper_quantile
        if lower_quantile < 0:
            lower_bound = prediction_point + lower_quantile
        else:
            lower_bound = prediction_point - lower_quantile
        return lower_bound, upper_bound
    
    lower_list = list()
    upper_list = list()
    for i in prediction_list:
        lo, hi = predict_new_point(i)
        lower_list.append(lo)
        upper_list.append(hi)

    #for i in range(len(lower_list)):
    #    print(lower_list[i], prediction_list[i],upper_list[i])
    
        predictions_result = []
    for i in range(len(lower_list)):
        predictions_result.append({
            "lower_bound": lower_list[i],
            "prediction": prediction_list[i],
            "upper_bound": upper_list[i]
        })

    return predictions_result
    #print(date_list)
