import os, joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models')
PIPELINE_PATH = os.path.join(MODEL_PATH, 'pipelines')
os.makedirs(PIPELINE_PATH, exist_ok=True)
os.makedirs(MODEL_PATH, exist_ok=True)

def train_demo_model(transactions_df, n_clusters=3):
    # transactions_df: pandas DataFrame with columns ['amount','category','date']
    X = transactions_df.copy()
    # simple features: amount, day_of_month, category encoded by hash
    X['day'] = pd.to_datetime(X['date']).dt.day
    X['cat_code'] = X['category'].apply(lambda x: abs(hash(x)) % 50)
    features = X[['amount','day','cat_code']].values
    pipeline = Pipeline([('scaler', StandardScaler()), ('kmeans', KMeans(n_clusters=n_clusters, random_state=42))])
    pipeline.fit(features)
    joblib.dump(pipeline, os.path.join(PIPELINE_PATH, 'mindset_kmeans.joblib'))
    return pipeline

def load_model():
    path = os.path.join(PIPELINE_PATH, 'mindset_kmeans.joblib')
    if os.path.exists(path):
        return joblib.load(path)
    return None

def predict_mindset(model, transactions_list):
    # transactions_list: list of dicts
    import pandas as pd
    if model is None:
        return {'error':'No model trained'}
    df = pd.DataFrame(transactions_list)
    if df.empty:
        return {'error':'No transactions'}
    df['day'] = pd.to_datetime(df['date']).dt.day
    df['cat_code'] = df['category'].apply(lambda x: abs(hash(x)) % 50)
    X = df[['amount','day','cat_code']].values
    labels = model.predict(X)
    # simple aggregation: most common label
    from collections import Counter
    c = Counter(labels)
    top = c.most_common(1)[0]
    return {'most_common_mindset_label': int(top[0]), 'counts': dict(c)}
