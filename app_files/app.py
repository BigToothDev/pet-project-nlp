from shiny import App, render, ui, reactive
import pandas as pd
import json
import plotly.graph_objs as go

# Load the dataset (assuming the JSON structure is similar to the original R code)
with open('dataset.json') as f:
    data = json.load(f)

# Convert the dataset to a pandas DataFrame
df = pd.json_normalize(data)

# Define the UI
app_ui = ui.page_fluid(
    ui.h1("Visualisation of the data"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_select("article_id_manual", "Select an article by ID:", [str(id) for id in df['ID']]),
            ui.input_text("keyword", "Search by keyword:", ""),
            ui.input_action_button("search_btn", "Find"),
            ui.input_select("article_id_search", "Select an article with your keyword:", []),
        ),
        ui.panel_main(
            ui.h3("Article title:"),
            ui.output_text("headline"),
            ui.h4("Date:"),
            ui.output_text("datetime"),
            ui.h4("URL:"),
            ui.output_text("link"),
            ui.h4("Tone of the article:"),
            ui.output_text("tone"),
            ui.h4("General sentiment:"),
            ui.output_text("general_sentiment"),
            ui.h4("Text of the article:"),
            ui.output_text("content"),
        ),
    ),
)

# Define the server logic
def server(input, output, session):

    @reactive.Calc
    def selected_article():
        article_id = input.article_id_manual()
        if article_id is None:
            return None
        return df[df['ID'] == int(article_id)].iloc[0]
    
    @output()
    @render.text
    def headline():
        article = selected_article()
        if article is not None:
            return article['article_data.headline']
        return ""

    @output()
    @render.text
    def content():
        article = selected_article()
        if article is not None:
            return article['article_data.content']
        return ""

    @output()
    @render.text
    def link():
        article = selected_article()
        if article is not None:
            return article['article_data.link']
        return ""

    @output()
    @render.text
    def datetime():
        article = selected_article()
        if article is not None:
            return article['article_data.datetime']
        return ""

    @output()
    @render.text
    def tone():
        article = selected_article()
        if article is not None:
            return f"Negative tone: {article['article_data.neg_tone']}\nNeutral tone: {article['article_data.neu_tone']}\nPositive tone: {article['article_data.pos_tone']}\nCompound tone: {article['article_data.compound_tone']}"
        return ""

    @output()
    @render.text
    def general_sentiment():
        article = selected_article()
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
    def update_article_search():
        if input.search_btn() is None or not input.keyword():
            return
        keyword = input.keyword()
        filtered_data = df[df['article_data.lemmatized_headline'].str.contains(keyword, case=False, na=False)]
        
        if len(filtered_data) > 0:
            session.update_input("article_id_search", options=[str(id) for id in filtered_data['ID']])
        else:
            session.update_input("article_id_search", options=[])

    @reactive.Effect
    def update_manual_article_id():
        article_id_search = input.article_id_search()
        if article_id_search:
            session.update_input("article_id_manual", value=article_id_search)

# Create and run the app
app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
