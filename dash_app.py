import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
from flask import Flask
from models import Transaction
from models import db
def create_dash(server):
    app = dash.Dash(__name__, server=server, url_base_pathname='/dash/')
    # sample layout
    app.layout = html.Div([
        html.H3('NeuroSpend AI — Demo Dashboard'),
        dcc.Dropdown(id='user-select', options=[{'label':'User 1','value':1}], value=1),
        dcc.Graph(id='spend-heatmap'),
        dcc.Graph(id='category-dist')
    ])

    @app.callback(
        dash.dependencies.Output('spend-heatmap','figure'),
        [dash.dependencies.Input('user-select','value')]
    )
    def update_heatmap(user_id):
        # load last 500 txns
        qs = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.date.desc()).limit(500).all()
        df = pd.DataFrame([t.to_dict() for t in qs])
        if df.empty:
            df = pd.DataFrame({'date':[], 'amount':[], 'category':[]})
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            df['hour'] = df['date'].dt.hour
            heat = df.groupby([df['date'].dt.date, 'category']).sum().reset_index()
            fig = px.bar(heat, x='date', y='amount', color='category', title='Spend over time by category')
        else:
            fig = px.scatter(title='No data')
        return fig

    @app.callback(
        dash.dependencies.Output('category-dist','figure'),
        [dash.dependencies.Input('user-select','value')]
    )
    def update_cat(user_id):
        qs = Transaction.query.filter_by(user_id=user_id).all()
        df = pd.DataFrame([t.to_dict() for t in qs])
        if df.empty:
            fig = px.pie(names=['No data'], values=[1], title='No data')
        else:
            fig = px.pie(df, names='category', values='amount', title='Category distribution')
        return fig

    return app
