import os
from app import create_app
from models import db, Transaction
import pandas as pd
from ml import train_demo_model
app = create_app()
with app.app_context():
    qs = Transaction.query.limit(1000).all()
    df = pd.DataFrame([t.to_dict() for t in qs])
    if df.empty:
        print('No transactions found. Run create_db.py first.')
    else:
        model = train_demo_model(df, n_clusters=4)
        print('Model trained and saved.')
