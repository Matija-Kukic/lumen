from fastapi import FastAPI, File, UploadFile
import pandas as pd
from predict import prediction
from pathlib import Path

app = FastAPI()

# Define FastAPI endpoints
@app.get("/")
async def read_root():
    return {"message": "Welcome to Room404! plz"}

@app.post("/predict/")
async def analyze_parquet(file: UploadFile = File(...)):

    if file.filename.endswith(".parquet"):
        # Read the contents of the Parquet file
        contents = await file.read()

        # Save the contents as test.parquet
        with open("test.parquet", "wb") as f:
            f.write(contents)
        
        # Load the saved Parquet file into a pandas DataFrame
        df = pd.read_parquet('test.parquet')

        prediction(df)

        # Analyze the DataFrame (example: calculating mean, median, etc.)
        '''
        analysis_result = {
            "columns": df.columns.tolist(),
            "num_rows": len(df),
        }
        return analysis_result
        '''
    else:
        return {"error": "Uploaded file must be a Parquet file"}
