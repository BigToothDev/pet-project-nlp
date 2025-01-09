import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import json
import plotly.graph_objs as go

with open('dataset.json') as f:
    data = json.load(f)

app = dash.Dash(__name__)

df = pd.json_normalize(data)

app.layout = html.Div([
    html.H1("Visualisation of the data"),
    html.Div([
        html.Div([
            html.Label("Select an article by ID:"),
            dcc.Dropdown(
                id='article_id_manual',
                options=[{'label': str(id), 'value': id} for id in df['ID']],
                value=None
            ),
            html.Label("Search by keyword:"),
            dcc.Input(id='keyword', type='text', value=''),
            html.Button("Find", id='search_btn'),
            html.Label("Select an article with your keyword:"),
            dcc.Dropdown(
                id='article_id_search',
                options=[],
                value=None
            )
        ], style={'width': '30%', 'display': 'inline-block'}),
        
        html.Div([
            html.H3("Article title:"),
            html.Div(id='headline'),
            html.H4("Date:"),
            html.Div(id='datetime'),
            html.H4("URL:"),
            html.Div(id='link'),
            html.H4("Tone of the article:"),
            html.Pre(id='tone'),
            html.H4("General sentiment:"),
            html.Div(id='general_sentiment'),
            html.H4("Text of the article:"),
            html.Div(id='content')
        ], style={'width': '60%', 'display': 'inline-block'})
    ])
])

@app.callback(
    [Output('headline', 'children'),
     Output('content', 'children'),
     Output('link', 'children'),
     Output('datetime', 'children'),
     Output('tone', 'children'),
     Output('general_sentiment', 'children')],
    [Input('article_id_manual', 'value')]
)
def update_article_info(article_id):
    if article_id is None:
        return "", "", "", "", "", ""
    
    article = df[df['ID'] == article_id].iloc[0]
    headline = article['article_data.headline']
    content = article['article_data.content']
    link = article['article_data.link']
    datetime = article['article_data.datetime']
    neg_tone = article['article_data.neg_tone']
    neu_tone = article['article_data.neu_tone']
    pos_tone = article['article_data.pos_tone']
    compound_tone = article['article_data.compound_tone']
    
    tone = f"Negative tone: {neg_tone}\nNeutral tone: {neu_tone}\nPositive tone: {pos_tone}\nCompound tone: {compound_tone}"
    
    general_sentiment = "Positive" if compound_tone >= 0.05 else ("Negative" if compound_tone <= -0.05 else "Neutral")
    
    return headline, content, link, datetime, tone, general_sentiment

@app.callback(
    Output('article_id_search', 'options'),
    [Input('search_btn', 'n_clicks')],
    [Input('keyword', 'value')]
)
def search_articles(n_clicks, keyword):
    if n_clicks is None or not keyword:
        return []
    
    filtered_data = df[df['article_data.lemmatized_headline'].str.contains(keyword, case=False, na=False)]
    
    if filtered_data.empty:
        return []
    
    return [{'label': str(id), 'value': id} for id in filtered_data['ID']]

@app.callback(
    Output('article_id_manual', 'value'),
    [Input('article_id_search', 'value')]
)
def update_manual_article_id(article_id_search):
    return article_id_search

if __name__ == '__main__':
    app.run_server(debug=True)