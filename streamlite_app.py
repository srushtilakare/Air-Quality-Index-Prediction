import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="🇮🇳 Smart AQI Intelligence System",
    page_icon="🌍",
    layout="wide"
)

# ---------------- CUSTOM STYLING ----------------
st.markdown("""
<style>
.main {background-color: #f4f6f9;}
h1 {color: #1f77b4;}
.stButton>button {background-color: #1f77b4; color: white;}
</style>
""", unsafe_allow_html=True)

st.title("🇮🇳 CPCB + AI Smart AQI Forecasting System")

# ---------------- LOAD MODEL ----------------
model = joblib.load("best_aqi_model.pkl")

# ---------------- SESSION STATE ----------------
if "aqi_history" not in st.session_state:
    st.session_state.aqi_history = [150, 150, 150]

# ---------------- ENTER YOUR API DETAILS ----------------
 
RESOURCE_ID = "3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69"

# ---------------- CITY DROPDOWN ----------------
st.subheader("🌐 Live CPCB Data")
city = st.selectbox("Select Indian City",
                    ["Delhi", "Mumbai", "Pune", "Bengaluru", "Kolkata", "Chennai"])

# ---------------- FETCH LIVE DATA ----------------
live_data = None

if st.button("Fetch Live CPCB Data"):

    url = f"https://api.data.gov.in/resource/{RESOURCE_ID}?api-key={API_KEY}&format=json&filters[city]={city}"

    try:
        response = requests.get(url)
        data = response.json()

        if "records" in data and len(data["records"]) > 0:
            df = pd.DataFrame(data["records"])
            live_data = df.iloc[0]

            st.success(f"Live AQI Data Loaded for {city}")

        else:
            st.warning("No live data available for selected city.")

    except:
        st.error("Error fetching CPCB data. Check API key or resource ID.")

# ---------------- INPUT SECTION ----------------
st.subheader("📊 Pollutant Values")

col1, col2, col3 = st.columns(3)

def get_value(key, default=0.0):
    if live_data is not None and key in live_data:
        try:
            return float(live_data[key])
        except:
            return default
    return default

with col1:
    pm25 = st.number_input("PM2.5", value=get_value("pm2_5", 100.0))
    pm10 = st.number_input("PM10", value=get_value("pm10", 200.0))
    no = st.number_input("NO", value=get_value("no", 30.0))

with col2:
    no2 = st.number_input("NO2", value=get_value("no2", 40.0))
    nox = st.number_input("NOx", value=get_value("nox", 60.0))
    nh3 = st.number_input("NH3", value=get_value("nh3", 20.0))

with col3:
    co = st.number_input("CO", value=get_value("co", 1.0))
    so2 = st.number_input("SO2", value=get_value("so2", 15.0))
    o3 = st.number_input("O3", value=get_value("o3", 80.0))

benzene = st.number_input("Benzene", value=get_value("benzene", 5.0))
toluene = st.number_input("Toluene", value=get_value("toluene", 10.0))

# ---------------- PREDICTION ----------------
if st.button("🔮 Predict Tomorrow's AQI"):

    aqi_lag1 = st.session_state.aqi_history[-1]
    aqi_roll3 = np.mean(st.session_state.aqi_history[-3:])

    input_df = pd.DataFrame([[pm25, pm10, no, no2, nox, nh3, co,
                              so2, o3, benzene, toluene,
                              aqi_lag1, aqi_roll3]],
                            columns=['PM2.5','PM10','NO','NO2','NOx','NH3','CO',
                                     'SO2','O3','Benzene','Toluene',
                                     'AQI_lag1','AQI_roll3'])

    prediction = model.predict(input_df)[0]
    st.session_state.aqi_history.append(prediction)

    st.subheader("🎯 AQI Gauge")

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prediction,
        gauge={
            'axis': {'range': [0, 500]},
            'steps': [
                {'range': [0, 50], 'color': "green"},
                {'range': [50, 100], 'color': "yellow"},
                {'range': [100, 200], 'color': "orange"},
                {'range': [200, 300], 'color': "red"},
                {'range': [300, 500], 'color': "purple"},
            ],
        }
    ))
    st.plotly_chart(fig)

    # ---------------- HEALTH ALERT ----------------
    if prediction > 300:
        st.error("🚨 Severe Pollution Expected!")
    elif prediction > 200:
        st.warning("⚠ Poor Air Quality Expected.")
    elif prediction > 100:
        st.info("Moderate Air Quality.")
    else:
        st.success("Good Air Quality Expected.")

    # ---------------- 5 DAY FORECAST ----------------
    st.subheader("📅 5-Day Forecast")

    forecast_values = []
    temp_history = st.session_state.aqi_history.copy()

    for i in range(5):
        lag1 = temp_history[-1]
        roll3 = np.mean(temp_history[-3:])
        future_input = input_df.copy()
        future_input['AQI_lag1'] = lag1
        future_input['AQI_roll3'] = roll3
        future_pred = model.predict(future_input)[0]
        forecast_values.append(future_pred)
        temp_history.append(future_pred)

    forecast_df = pd.DataFrame({
        "Day": [f"Day {i+1}" for i in range(5)],
        "Predicted AQI": forecast_values
    })

    st.line_chart(forecast_df.set_index("Day"))

    # ---------------- FEATURE IMPORTANCE ----------------
    if hasattr(model, "feature_importances_"):
        st.subheader("📊 Feature Importance")
        importance = pd.DataFrame({
            "Feature": input_df.columns,
            "Importance": model.feature_importances_
        }).sort_values(by="Importance", ascending=False)

        st.bar_chart(importance.set_index("Feature"))

    # ---------------- PDF REPORT ----------------
    st.subheader("📄 Download AQI Report")

    file_path = "AQI_Report.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Smart AQI Forecast Report", styles['Heading1']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"City: {city}", styles['Normal']))
    elements.append(Paragraph(f"Predicted AQI: {prediction:.2f}", styles['Normal']))

    doc.build(elements)

    with open(file_path, "rb") as f:
        st.download_button("Download PDF Report", f, file_name="AQI_Report.pdf")

st.markdown("---")
st.markdown("Developed by Srushti Lakare | AI + CPCB Real-Time Forecasting System")
