import os
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from models import db, User, Transaction, Mindset
from ml import load_model, predict_mindset
from dash_app import create_dash
from utils import text_query_to_sql, fetch_youtube_videos
# pocketsphinx import for local STT
try:
    from pocketsphinx import AudioFile
    POCKET_AVAILABLE = True
except Exception:
    POCKET_AVAILABLE = False

load_dotenv()

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    database_url = os.getenv('DATABASE_URL', 'sqlite:///neurospend.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # register Dash
    create_dash(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api/transactions', methods=['GET'])
    def list_txns():
        user_id = request.args.get('user_id', 1)
        txns = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.date.desc()).limit(500).all()
        return jsonify([t.to_dict() for t in txns])

    @app.route('/api/predict', methods=['POST'])
    def predict():
        data = request.json or {}
        user_id = data.get('user_id', 1)
        # simple predict using model
        model = load_model()
        transactions = Transaction.query.filter_by(user_id=user_id).all()
        df_input = [t.to_dict() for t in transactions]
        preds = predict_mindset(model, df_input)
        return jsonify(preds)

    @app.route('/api/voice_query', methods=['POST'])
    def voice_query():
        # Accepts JSON {"text": "show me my expenses last month"} OR audio (placeholder)
        payload = request.json or {}
        text = payload.get('text')
        if not text:
            return jsonify({'error':'No text provided. For production, send audio and implement STT.'}), 400
        # Convert text -> SQL-like instructions (very basic)
        sql_info = text_query_to_sql(text)
        # Execute basic query using SQLAlchemy (limited mapping)
        # Example supports "last month" or "this month" + "expenses"
        if sql_info.get('type') == 'expenses_last_month':
            from sqlalchemy import func
            import datetime
            today = datetime.date.today()
            first = (today.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
            last = today.replace(day=1) - datetime.timedelta(days=1)
            rows = Transaction.query.filter(Transaction.date >= first, Transaction.date <= last).all()
            import pandas as pd
            df = pd.DataFrame([r.to_dict() for r in rows])
            # simple aggregation
            total = df['amount'].sum() if not df.empty else 0
            return jsonify({'summary':'expenses_last_month', 'total': float(total), 'count': len(df)})
        return jsonify({'message':'Query parsed', 'sql_info': sql_info})

    @app.route('/api/youtube_recs', methods=['GET'])
    def youtube_recs():
        topic = request.args.get('topic', 'personal finance')
        key = os.getenv('YOUTUBE_API_KEY')
        if not key:
            return jsonify({'error':'Missing YOUTUBE_API_KEY env variable'}), 400
        vids = fetch_youtube_videos(topic, api_key=key, max_results=5)
        return jsonify(vids)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
