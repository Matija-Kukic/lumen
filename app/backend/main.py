from fastapi import FastAPI, File, UploadFile
import pandas as pd
from predict import prediction
from pathlib import Path

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to Room404!"}

@app.post("/predict/")
async def analyze_parquet(file: UploadFile = File(...)):

    if file.filename.endswith(".parquet"):
        contents = await file.read()

        with open("test.parquet", "wb") as f:
            f.write(contents)
        
        df = pd.read_parquet('test.parquet')

        date_list, prediction_list, upper_list, lower_list, room_occ = prediction(df)
        res = {
            "predictions": prediction_list,
            "date" : date_list,
            "upper" : upper_list,
            "lower" : lower_list,
            "occ" : room_occ
        }
        
        return res
    else:
        return {"error": "Uploaded file must be a Parquet file"}
