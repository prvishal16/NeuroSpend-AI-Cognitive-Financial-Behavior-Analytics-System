📌 NeuroSpend AI — Cognitive Financial Behavior Analytics System
AI-powered transaction intelligence, voice-controlled analytics, ML pipelines & financial insights engine.
🚀 Overview

NeuroSpend AI is an advanced full-stack financial behavior analytics system combining:

MySQL + SQLAlchemy ORM

Python + Flask REST API

Plotly Dash Dashboards

Machine Learning Pipelines (scikit-learn)

Voice Commands (Pocketsphinx STT)

Automated Training with Apache Airflow

Google YouTube Recommendations API

This project transforms raw transaction data into actionable insights, predictions, and personalized financial coaching.

🧠 Features
🔹 1. Voice-Controlled Analytics

Supports .wav uploads

Uses Pocketsphinx for offline speech-to-text

Queries like:

“Show expenses last month”

“Category-wise spending”

“Total food expenses this week”

🔹 2. ML-Based Behavioral Classification

KMeans clustering

Category encodings + date-time features

Predicts behavioral patterns:

Impulse Spending

Overspending Risk

Savings-oriented Behavior

Time-of-day spikes

🔹 3. Plotly Dash Dashboard

Category distribution pie charts

Spending heatmaps

Daily/weekly trend bars

Real-time visualization of predictions

🔹 4. SQL Analytics Engine

Window functions

Periodic aggregations

Rolling averages

Automated anomaly detection

🔹 5. Airflow ML Training

Daily training job (neurospend_train_pipeline)

Regenerates joblib models

Keeps analytics fresh and accurate

🔹 6. Google YouTube Financial Recommendations

Searches for “budgeting tips”, “saving habits”, etc

Personalized based on detected behavior type

📂 Project Structure
neurospend_starter/
│── app.py
│── models.py
│── ml.py
│── utils.py
│── dash_app.py
│── create_db.py
│── train_model.py
│── airflow/
│   └── dags/train_pipeline.py
│── templates/index.html
│── static/
│── requirements.txt
│── README.md

🛠 Installation
python -m venv venv
source venv/bin/activate       # or venv\Scripts\activate
pip install -r requirements.txt

💾 Initialize Database
python create_db.py

🤖 Train ML Model
python train_model.py

▶ Run App
flask run --host=0.0.0.0 --port=5000


Dashboard opens at:
👉 http://localhost:5000/dash/

🎤 Voice Query API Example
POST /api/voice_query
Form Data:
 audio: sample.wav

▶ YouTube Financial Tips API
GET /api/youtube_recs?topic=personal finance

📸 Sample Screenshots (How It Will Look)

Here are representative images of exactly how your Dash dashboard will look (using the layout we coded):

Dashboard Home
