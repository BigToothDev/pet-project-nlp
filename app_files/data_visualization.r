library(shiny)
library(jsonlite)
library(dplyr)

data <- fromJSON("dataset.json")

ui <- fluidPage(
  titlePanel("Visualisation of the data"),
  sidebarLayout(
    sidebarPanel(
      selectInput("article_id_manual", "Select an article by ID:", choices = data$ID),
      textInput("keyword", "Search by keyword:", ""),
      actionButton("search_btn", "Find"),
      selectInput("article_id_search", "Select an article with your keyword:", choices = NULL)
    ),
    mainPanel(
      h3("Article title:"),
      textOutput("headline"),
      h4("Date:"),
      verbatimTextOutput("datetime"),
      h4("URL:"),
      verbatimTextOutput("link"),
      h4("Tone of the article:"),
      verbatimTextOutput("tone"),
      h4("General sentiment:"),
      verbatimTextOutput("general_sentiment"),
      h4("Text of the article:"),
      textOutput("content")
    )
  )
)

server <- function(input, output, session) {
  
  selected_article <- reactive({
    req(input$article_id_manual)
    article <- data[data$ID == input$article_id_manual, ]
    return(article)
  })
  
  output$headline <- renderText({
    article <- selected_article()
    article$article_data$headline
  })
  
  output$content <- renderText({
    article <- selected_article()
    article$article_data$content
  })
  
  output$link <- renderText({
    article <- selected_article()
    article$article_data$link
  })
  
  output$datetime <- renderText({
    article <- selected_article()
    article$article_data$datetime
  })
  
  output$tone <- renderPrint({
    article <- selected_article()
    paste("Negative tone:", article$article_data$neg_tone,
          "Neutral tone:", article$article_data$neu_tone,
          "Positive tone:", article$article_data$pos_tone,
          "Compound tone:", article$article_data$compound_tone)
  })
  
  output$general_sentiment <- renderText({
    article <- selected_article()
    compound <- article$article_data$compound_tone
    if (compound >= 0.05) {
      "Positive"
    } else if (compound <= -0.05) {
      "Negative"
    } else {
      "Neutral"
    }
  })
  
  observeEvent(input$search_btn, {
    req(input$keyword)
    keyword <- input$keyword
    
    filtered_data <- data %>%
      filter(grepl(keyword, article_data$lemmatized_headline, ignore.case = TRUE))
    
    if (nrow(filtered_data) > 0) {
      updateSelectInput(session, "article_id_search", choices = filtered_data$ID)
    } else {
      updateSelectInput(session, "article_id_search", choices = NULL)
      showNotification("No results found", type = "error")
    }
  })
  
  observe({
    req(input$article_id_search)
    article <- data[data$ID == input$article_id_search, ]
    updateSelectInput(session, "article_id_manual", selected = article$ID)
  })
}

shinyApp(ui = ui, server = server)
