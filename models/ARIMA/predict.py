import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib as jl
from datetime import datetime,timedelta
from pathlib import Path
import math
def main():
    model = jl.load('arima_trained.pkl')
    df = pd.read_parquet('test.parquet')
     
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
    end = int((date2-date1).days) + start - 1
    #print(start,end,date1,date2)
    pred = model.predict(start+366,end+366)
    #print(pred)


    path = Path.cwd().parent.parent
    filePath = str(path) + "/data_cleanup/second_dataset/train_data_price_corrected.parquet"
    df2 = pd.read_parquet(filePath)
    path = Path.cwd().parent.parent
    filePath = str(path) + "/data_cleanup/second_dataset/train_data_price_corrected.parquet"
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
    train = pd.concat([train, train.copy()], ignore_index=True) 
    test = pd.concat([test, test.copy()], ignore_index=True) 
    #print(train)
    test_list =  test["room_cnt"].tolist()
    train_list = train["room_cnt"].tolist()
    mid_point_test = list()
    for i in range(end-start):
        mid_point_test.append((test_list[i] + train_list[i]) / 2)
    prediction_list = list()
    for i, data in enumerate(train["room_count_log"]):
        if i >= start and i <= end:
            prediction_list.append(data)
            #print("test05",data)
        else:
            continue
    #print("test",len(prediction_list),len(pred),start,end)
    for i, prediction in enumerate(pred):
        #print("test2",i)
        prediction_list[i] += prediction
    for i in range(len(prediction_list)):
        prediction_list[i] = math.exp(prediction_list[i])

    residuals = list()
    residuals_list = residuals

    for i in range(len(mid_point_test)):
        residuals.append(mid_point_test[i]-prediction_list[i])
    residuals_sorted = np.sort(residuals_list)
   
    p_values = [(np.sum(residuals_list >= r) + 1) / (len(residuals_list) + 1) for r in residuals_sorted]
    alpha = 0.1
     
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
    #print(date_list)
    sd = min(date_list)
    ed = max(date_list)
    print(len(prediction_list),len(date_list),start,end,date_list[len(date_list)-1])
    plt.figure(figsize=(50, 10))
    plt.plot(date_list, prediction_list,color = "red")
    plt.plot(date_list, upper_list,color = "orange")
    plt.plot(date_list, lower_list,color = "orange")
    plt.plot(date_list, room_occupancy["room_cnt"], color="blue")
    plt.fill_between(date_list, upper_list, lower_list, color='gray', alpha=0.3)

    plt.title("Ukupan broj zauzetih soba")
    plt.xlabel("Datum")
    plt.ylabel("Ukupan broj gostiju")
    plt.xticks(rotation = 45) 
    plt.tight_layout()  
    plt.show()
if __name__ == "__main__":
    main()
