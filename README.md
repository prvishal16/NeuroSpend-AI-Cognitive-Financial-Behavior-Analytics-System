# NeuroSpend AI — Starter Kit (VoiceSpend extension)
## Overview
This starter project contains a minimal production-like skeleton for a Cognitive Financial Behavior Analytics System.
It includes:
- Flask app with SQLAlchemy (configurable to MySQL via `SQLALCHEMY_DATABASE_URI`)
- ML pipeline using scikit-learn (clustering + simple risk model) persisted with joblib
- Plotly Dash dashboard embedded into Flask
- Voice/chat endpoint skeleton (accepts text queries; audio handling placeholder)
- Google YouTube API integration placeholder to fetch personalized video recommendations

## How to run (development)
1. Create a virtual environment and install requirements:
   ```
   python -m venv venv
   source venv/bin/activate      # on Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. (Optional) Configure a MySQL database by setting environment variable `DATABASE_URL`
   Example: `export DATABASE_URL='mysql+pymysql://user:pass@host:3306/neurospend'`
   If unset, the app uses local SQLite at `sqlite:///neurospend.db`.
3. Initialize DB and seed sample data:
   ```
   python create_db.py
   ```
4. Train demo ML model:
   ```
   python train_model.py
   ```
5. Run the Flask app:
   ```
   flask run --host=0.0.0.0 --port=5000
   ```
   Or with gunicorn:
   ```
   gunicorn -w 4 "app:create_app()"
   ```
6. Open the Dash UI at http://localhost:5000/dash

## Files
- app.py: Flask application factory + API endpoints
- models.py: SQLAlchemy models (User, Transaction, Mindset)
- ml.py: ML pipeline utilities (train, predict)
- dash_app.py: Plotly Dash app integrated into Flask
- create_db.py: Initialize DB and seed sample transactions
- train_model.py: Demo training script (creates models/joblib files)
- utils.py: helper functions (text->query mapping, YouTube API)
- requirements.txt
- README.md

## Notes
- The voice endpoint currently accepts plain text queries. For production voice support, add client-side recording and send audio to a speech-to-text service (Web Speech API, Google Speech-to-Text, or SpeechRecognition library + local pocketsphinx).
- The Google YouTube integration requires an API key. Place it in environment variable `YOUTUBE_API_KEY`.
- This is a starting point. Extend the ML models, SQL windowed queries, and dashboards to match NeuroSpend AI full spec.
