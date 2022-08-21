# Prevendo Ações
Dashboard de ações

## Indice
* [Instalação](#Instalação)

# Instalação
Para executar os algoritmos dese repositório recomenda-se a 
instalação dos pacotes contidos no arquivo requirements.txt

## 📦 Passos para instalar os pacotes

1. Ative seu ambiente virtual.
2. Caminhe até o diretório do arquivo requirements.txt
3. Execute o comando abaixo

```
conda install yfinance 
pip install streamlit
conda install plotly
conda install -c anaconda ephem
conda install -c conda-forge pystan
conda install -c conda-forge fbprophet
```

## Como executar o aplicativo

```
streamlit run model.py
```

