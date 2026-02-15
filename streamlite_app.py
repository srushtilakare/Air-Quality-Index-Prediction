import streamlit as st
import joblib
import numpy as np
import pandas as pd

st.title("AQI Forecasting App (Next-Day Prediction)")

# Load model
model = joblib.load("best_aqi_model.pkl")

# Initialize AQI history
if "aqi_history" not in st.session_state:
    st.session_state.aqi_history = [150, 150, 150]  # initial dummy values

st.subheader("Enter Today's Pollutant Values")

pm25 = st.number_input("PM2.5", value=100.0)
pm10 = st.number_input("PM10", value=200.0)
no = st.number_input("NO", value=30.0)
no2 = st.number_input("NO2", value=40.0)
nox = st.number_input("NOx", value=60.0)
nh3 = st.number_input("NH3", value=20.0)
co = st.number_input("CO", value=1.0)
so2 = st.number_input("SO2", value=15.0)
o3 = st.number_input("O3", value=80.0)
benzene = st.number_input("Benzene", value=5.0)
toluene = st.number_input("Toluene", value=10.0)

if st.button("Predict Tomorrow's AQI"):

    # Compute lag and rolling
    aqi_lag1 = st.session_state.aqi_history[-1]
    aqi_roll3 = np.mean(st.session_state.aqi_history[-3:])

    # Create input dataframe
    input_data = pd.DataFrame([[
        pm25, pm10, no, no2, nox, nh3, co,
        so2, o3, benzene, toluene,
        aqi_lag1, aqi_roll3
    ]], columns=[
        'PM2.5','PM10','NO','NO2','NOx','NH3','CO',
        'SO2','O3','Benzene','Toluene',
        'AQI_lag1','AQI_roll3'
    ])

    prediction = model.predict(input_data)[0]

    st.success(f"Predicted AQI for Tomorrow: {prediction:.2f}")

    # Update history
    st.session_state.aqi_history.append(prediction)
