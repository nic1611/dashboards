import warnings
warnings.filterwarnings('ignore')  # Hide warnings
import datetime as dt
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import plotly.express as px
import streamlit as st
from datetime import date
import datetime

st.title('Análise de preço de criptoativos')

st.sidebar.header('Escolha as datas')

today = datetime.date.today()
start = st.sidebar.date_input('Data Início', datetime.date(today.year - 1, today.month, today.day))
end = st.sidebar.date_input('Data Fim', today)

#bitcoin
btc = web.DataReader("BTC-USD", 'yahoo', start, end)  # Collects data
btc.reset_index(inplace=True)
crypto= btc[['Date','Adj Close']]
crypto= crypto.rename(columns = {'Adj Close':'Bitcoin_BTC'})
crypto[ 'BTC_7DAY_MA' ] = crypto.Bitcoin_BTC.rolling( 7).mean()

#Ethereum
eth = web.DataReader("ETH-USD", 'yahoo', start, end)  # Collects data
eth.reset_index(inplace=True)
crypto["Ethereum_ETH"] = eth["Adj Close"]
crypto[ 'ETH_7DAY_MA' ] = crypto.Ethereum_ETH.rolling( 7).mean()

#Cardano
ada = web.DataReader("ADA-USD", 'yahoo', start, end)  # Collects data
ada.reset_index(inplace=True)
crypto["Cardano_ADA"]= ada["Adj Close"]
crypto[ 'ADA_7DAY_MA' ] = crypto.Cardano_ADA.rolling( 7).mean()

#Dash
dash = web.DataReader("DASH-USD", 'yahoo', start, end)  # Collects data
dash.reset_index(inplace=True)
crypto["DASH"]= dash["Adj Close"]
crypto[ 'DASH_7DAY_MA' ] = crypto.DASH.rolling( 7).mean()

#ATOM-USD
dash = web.DataReader("ATOM-USD", 'yahoo', start, end)  # Collects data
dash.reset_index(inplace=True)
crypto["ATOM"]= dash["Adj Close"]
crypto[ 'ATOM_7DAY_MA' ] = crypto.ATOM.rolling( 7).mean()

crypto.set_index("Date", inplace=True)

fig1 = px.line(crypto, y=['Bitcoin_BTC','Ethereum_ETH','Cardano_ADA','DASH','ATOM'] )
fig2 = px.line(crypto, y=['BTC_7DAY_MA', 'ETH_7DAY_MA', 'ADA_7DAY_MA', 'DASH_7DAY_MA', 'ATOM_7DAY_MA'] )

st.subheader('Último preço')
for col in ['Bitcoin_BTC','Ethereum_ETH','Cardano_ADA','DASH','ATOM']:
    st.write('{:}: {:.2f}'.format(col, crypto[col].iloc[-1]))

st.subheader('Grafico de preços')
st.plotly_chart(fig1)

st.subheader('Grafico de Valores Médios Móveis')
st.plotly_chart(fig2)
