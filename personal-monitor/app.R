library(shiny)
library(shinythemes)
library(rsconnect)
source("./src/scrapy.R")

ui <- fluidPage(
    theme = shinytheme("superhero"),
    titlePanel("Personal Monitor"),
    
    sidebarLayout(
        sidebarPanel(
            selectInput("escolhaMoeda","Moeda",
                        list("Ethereum" = "ethereum-eth", 
                             "Eos" = "eos-eos", 
                             "Iost" = "iost-iost", 
                             "Tron" = "tron-trx", 
                             "Dash" = "dash-dash", 
                             "Cosmos" = "cosmos-atom", 
                             "Neo" = "neo-neo", 
                             "Stellar" = "stellar-xlm")),
        ),
        
        mainPanel(
            htmlOutput("valorMoeda")
        )
    )
)

server <- function(input, output) {
    
    output$valorMoeda <- renderUI({HTML(
        paste(
            "<h1>Valor: R$ ",getCrypto(input$escolhaMoeda),"</h1>",
            "<br/><h4>Mais informações</h4><a href='",getMoreInfo(input$escolhaMoeda),"' target='_blank'>Clique aqui</a>", sep = ""
                  ))})
}

shinyApp(ui = ui, server = server)
