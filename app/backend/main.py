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

        predictions_result = prediction(df)

        analysis_result = {
            "predictions": predictions_result,
        }
        return analysis_result
    else:
        return {"error": "Uploaded file must be a Parquet file"}
