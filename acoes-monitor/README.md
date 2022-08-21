# Ações Monitor
##### Sistema de monitoramento de ações
##### Este é um Aplicativo utilizado para exibir e monitorar ações por meio de uma solução web

## Localize
<!-- * [Imagens](#imagens) -->
* [Instalação](#instalação)
* [Tecnologias](#tecnologias)

<!-- ## Imagens
![Alt text](/static/sistema-previsao.PNG?raw=true "Tela de produto") -->

## Instalação
##### Acesse o site do Bovespa e baixe os arquivos dos anos que deseja.
##### Descompacte os arquivos na pasta 'COTAHIST'.
##### Garanta que os arquivos estão nomeados como 'COTAHIST_A{ano}.TXT'
[Histórico Bovespa](http://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-a-vista/series-historicas/)

##### Após clonar o repositório digite os comandos: 

```bash
$ python -m venv venv
$ source <venv>/bin/activate
$ pip install -r requirements.txt
$ python etl.py
$ streamlit run app_risco.py
```


## Tecnologias
* [python](https://www.python.org/)
* [pandas](https://pandas.pydata.org/)
* [streamlit](https://www.streamlit.io/) 
