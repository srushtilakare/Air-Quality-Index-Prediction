Smart AQI Intelligence & Forecasting Dashboard

An AI-powered Air Quality Index (AQI) forecasting system integrated with real-time Government of India CPCB data.

This project combines:

🇮🇳 CPCB Real-Time Data (data.gov.in API)

🤖 Machine Learning Model (Random Forest Regression)

📊 Feature Engineering (Lag & Rolling Features)

📅 5-Day Recursive Forecast

🎯 Interactive AQI Gauge Meter

📈 Feature Importance Visualization

📄 PDF Report Generation

🖥 Professional Streamlit Dashboard UI

🚀 Live Features
📊 Real-Time CPCB Data

Fetch live AQI data from the Government of India Open Data Portal.

🔮 Next-Day AQI Prediction

Predict tomorrow’s AQI using:

Pollutant concentrations

AQI lag feature (previous day)

3-day rolling average

📅 5-Day Forecast

Recursive multi-step forecasting based on model predictions.

🎯 AQI Gauge Visualization

Speedometer-style visualization for intuitive AQI interpretation.

📈 Model Analytics

Feature importance graph for interpretability.

📄 PDF Report Generation

Download forecast report instantly.

🧠 Machine Learning Details

Model: Random Forest Regressor

Target Variable: Next-Day AQI

Features:

PM2.5

PM10

NO

NO2

NOx

NH3

CO

SO2

O3

Benzene

Toluene

AQI_lag1

AQI_roll3

🏗 System Architecture

CPCB Real-Time Data
↓
Feature Engineering (Lag + Rolling)
↓
ML Model Prediction
↓
Dashboard Visualization
↓
5-Day Forecast + PDF Report

📂 Project Structure
Air-Quality-Index-Prediction/
│
├── streamlite_app.py
├── best_aqi_model.pkl
├── requirements.txt
├── .gitignore
└── README.md

⚙ Installation
1️⃣ Clone Repository
git clone https://github.com/yourusername/Air-Quality-Index-Prediction.git
cd Air-Quality-Index-Prediction

2️⃣ Create Virtual Environment
python -m venv aqi_env
aqi_env\Scripts\activate   (Windows)

3️⃣ Install Requirements
pip install -r requirements.txt

🔐 API Configuration

Create a .env file:

API_KEY=your_data_gov_api_key


Dataset Used:

Real Time Air Quality Index from various locations (CPCB)

Source: https://data.gov.in

▶ Run Application
streamlit run streamlite_app.py


App will open at:

http://localhost:8501

📊 Example Dashboard Modules

📊 Live Data Tab

🔮 Prediction Tab

📅 5-Day Forecast

📈 Analytics

📄 Report Generator

🛠 Technologies Used

Python

Streamlit

Scikit-learn

Pandas

NumPy

Plotly

ReportLab

Government Open Data API

🔒 Security Notes

API keys are not committed to GitHub.

.gitignore prevents sensitive file uploads.

Model version compatibility maintained.

📈 Future Improvements

🌍 India AQI Map Visualization

📡 Auto-refresh live data

🧠 LSTM Deep Learning Model

☁ Cloud Deployment

📊 Historical Data Storage

 