import streamlit as st
import requests
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt

st.title('Room404 Occupancy Prediction')

uploaded_file = st.file_uploader("Upload Parquet file", type=["parquet"])

if uploaded_file is not None:
   # Display a message while the file is being uploaded
   st.text("Uploading file...")

   # Make the POST request to the FastAPI backend
   response = requests.post("http://backend:8000/predict/", files={"file": uploaded_file})

   if response.status_code == 200:
      # If the request is successful, display the analysis results
      res = response.json()
      dates = res["date"]
      datetime_objects = [datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S') for ts in dates]
      dates = datetime_objects
      preds = res["predictions"]
      upper = res["upper"]
      lower = res["lower"]
      occ = res["occ"]
      st.text("Blue line - given data")
      st.text("Red line - prediction data")
      plt.figure(figsize=(100, 20))
      plt.plot(dates, preds,color = "red")
      plt.plot(dates, upper,color = "orange")
      plt.plot(dates, lower,color = "orange")
      plt.plot(dates, occ, color="blue")
      plt.fill_between(dates, upper, lower, color='gray', alpha=0.3)
      plt.title("Ukupan broj zauzetih soba")
      plt.xlabel("Datum")
      plt.ylabel("Ukupan broj gostiju")
      plt.xticks(rotation = 90)  
      plt.savefig('plot.png')
      st.image("plot.png", width = 1280, use_column_width=True, output_format="auto")
      
      for i in range(len(preds)):
         st.text(str(dates[i].date()))
         st.text("True value: " + str(round(occ[i]))+ " Prediction: "+ str(round(preds[i]))+ " Upper: "+ str(round(upper[i]))+ " Lower: " + str(round(lower[i])))
      #st.write(analysis_result)

   else:
      # If there's an error, display the error message
      st.error(f"Error: {response.text}")
