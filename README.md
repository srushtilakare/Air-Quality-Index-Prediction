** Smart AQI Intelligence Dashboard**

AI-powered Air Quality Index (AQI) Forecasting System integrated with real-time CPCB (Government of India) data.

_Features_

🇮🇳 Real-Time CPCB AQI Data (data.gov.in API)

🔮 Next-Day AQI Prediction (ML Model)

📅 5-Day Recursive Forecast

🎯 Interactive AQI Gauge Meter

📊 Feature Importance Visualization

📄 PDF Report Generation

🖥 Professional Multi-Tab Streamlit Dashboard

🧠 Machine Learning

Model: Random Forest Regressor

Features: Pollutants + AQI Lag + Rolling Mean

Target: Next-Day AQI

_⚙️ Run Locally_
git clone https://github.com/yourusername/Air-Quality-Index-Prediction.git
cd Air-Quality-Index-Prediction
pip install -r requirements.txt
streamlit run streamlite_app.py

_🔐 API Setup_

Get API key from:

👉 https://data.gov.in

Use dataset:
Real Time Air Quality Index from various locations (CPCB)

_🛠 Tech Stack_

Python • Streamlit • Scikit-learn • Pandas • Plotly • ReportLab
