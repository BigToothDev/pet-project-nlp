from shiny import App, render, ui, reactive
from pathlib import Path
import pandas as pd
import json

appdir = Path(__file__).parent

file_path = appdir / 'dataset.json'
with open(file_path, 'r', encoding='utf-8-sig') as file:
    ds = json.load(file)

df = pd.json_normalize(ds)

app_ui = ui.page_fluid(
    ui.panel_title("DataExplorer"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.h6("Total amount of articles:"),
            ui.output_text_verbatim("num_articles"),
            ui.input_selectize("article_id", "Select an article by ID:", [str(id) for id in df["ID"]]),
            ui.br(),
            ui.input_text("keyword", "Search by keyword:", ""),
            ui.input_action_button("search_btn", "Find"),
            ui.input_selectize("article_id_search", "Articles matching keyword:", []),
            ui.input_action_button("clear_btn", "Clear Selection"),
        ),
        ui.h3("Article Title:"),
        ui.output_text_verbatim("headline"),
        ui.h4("Date:"),
        ui.output_text_verbatim("datetime"),
        ui.h4("URL:"),
        ui.output_text_verbatim("link"),
        ui.h4("General sentiment:"),
        ui.output_text_verbatim("general_sentiment"),
        ui.h4("Tone of the article:"),
        ui.output_text_verbatim("tone"),
        ui.h4("Text of the article:"),
        ui.output_text("content"),
    ),
)

def server(input, output, session):
    @output()
    @render.text
    def num_articles():
        return len(ds)
    
    @reactive.Calc
    def select_article_by_id():
        article_id = input.article_id_search() or input.article_id() 
        if article_id is None:
            return None
        filtered = df[df["ID"] == int(article_id)]
        if not filtered.empty:
            return filtered.iloc[0].to_dict()
        return None

    @output()
    @render.text
    def headline():
        article = select_article_by_id()
        if article:
            return article.get('article_data.headline', "No headline available")
        return "No article selected"
    @output()
    @render.text
    def content():
        article = select_article_by_id()
        if article is not None:
            return article['article_data.content']
        return "No article selected"
    @output()
    @render.text
    def link():
        article = select_article_by_id()
        if article is not None:
            return article['article_data.link']
        return ""
    @output()
    @render.text
    def datetime():
        article = select_article_by_id()
        if article is not None:
            return article['article_data.datetime']
        return ""
    @output()
    @render.text
    def tone():
        article = select_article_by_id()
        if article is not None:
            return f"Negative tone: {article['article_data.neg_tone']}\nNeutral tone: {article['article_data.neu_tone']}\nPositive tone: {article['article_data.pos_tone']}\nCompound tone: {article['article_data.compound_tone']}"
        return ""
    @output()
    @render.text
    def general_sentiment():
        article = select_article_by_id()
        if article is not None:
            compound_tone = article['article_data.compound_tone']
            if compound_tone >= 0.05:
                return "Positive"
            elif compound_tone <= -0.05:
                return "Negative"
            else:
                return "Neutral"
        return ""
    
    @reactive.Effect
    def search_kw():
        if not input.search_btn():
            return
        keyword = input.keyword()
        if keyword:
            filtered_data = df[df['article_data.lemmatized_headline'].str.contains(keyword, case=False, na=False)]
            ui.update_selectize(
                session=session,
                id="article_id_search",
                choices=[str(id) for id in filtered_data['ID']] if not filtered_data.empty else [],
            )
            ui.update_selectize(
                session=session,
                id="article_id",
                choices=[]
            )

    @reactive.Effect
    def clear_selectize():
        if input.clear_btn():
            ui.update_selectize(
                session=session,
                id="article_id_search",
                choices=[]
            )
            ui.update_selectize(
                session=session,
                id="article_id",
                choices=[str(id) for id in df["ID"]]
            )
app = App(app_ui, server)
