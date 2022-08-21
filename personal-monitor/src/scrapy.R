library(rvest)

baseUrl <- "https://www.infomoney.com.br/cotacoes/"

getCrypto <- function(coin){
  page <- read_html(paste(baseUrl,coin,"/", sep = ""))
  
  price <- page %>% html_nodes(".value") %>% html_nodes("p") %>% html_text()
  
  price
}

getMoreInfo <- function(coin){
  paste(baseUrl,coin,"/grafico/", sep = "")
}