import streamlit as st
import requests

st.title('Room404 Occupancy Prediction')

uploaded_file = st.file_uploader("Upload Parquet file", type=["parquet"])

if uploaded_file is not None:
   # Display a message while the file is being uploaded
   st.text("Uploading file...")

   # Make the POST request to the FastAPI backend
   response = requests.post("http://backend:8000/predict/", files={"file": uploaded_file})

   if response.status_code == 200:
      # If the request is successful, display the analysis results
      analysis_result = response.json()
      st.text("Analysis Result (dictionary):")
      st.write(analysis_result)

   else:
      # If there's an error, display the error message
      st.error(f"Error: {response.text}")
