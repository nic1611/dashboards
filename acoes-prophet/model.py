import streamlit as st
import yfinance as yf
from datetime import date
import pandas as pd
from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly
from plotly import graph_objs as go

DATA_INICIO = '2017-01-01'
DATA_FIM = date.today().strftime('%Y-%m-%d')

# def pegar_dados_acoes():
#   path = 'acoes.csv'
#   return pd.read_csv(path, delimiter=';')

# df = pegar_dados_acoes()

def transform_filter_data(df):

  df = df[['Ação','Empresa','Preço','Margem EBIT','P/VPA','EV/EBIT','Div.Yield','Volume Financ.(R$)']]

  df['Preço'] = df['Preço'].str.replace('.','')
  df['Preço'] = df['Preço'].str.replace(',','.')
  df['Preço'] = pd.to_numeric(df['Preço'])

  df['P/VPA'] = df['P/VPA'].str.replace('.','')
  df['P/VPA'] = df['P/VPA'].str.replace(',','.')
  df['P/VPA'] = pd.to_numeric(df['P/VPA'])

  df['EV/EBIT'] = df['EV/EBIT'].str.replace('.','')
  df['EV/EBIT'] = df['EV/EBIT'].str.replace(',','.')
  df['EV/EBIT'] = pd.to_numeric(df['EV/EBIT'])

  df['Volume Financ.(R$)'] = df['Volume Financ.(R$)'].str.replace('.','')
  df['Volume Financ.(R$)'] = df['Volume Financ.(R$)'].str.replace(',','.')
  df['Volume Financ.(R$)'] = pd.to_numeric(df['Volume Financ.(R$)'])

  df['Margem EBIT'] = df['Margem EBIT'].str.replace('%','')
  df['Margem EBIT'] = df['Margem EBIT'].str.replace('.','')
  df['Margem EBIT'] = df['Margem EBIT'].str.replace(',','.')
  df['Margem EBIT'] = pd.to_numeric(df['Margem EBIT'])

  df['Div.Yield'] = df['Div.Yield'].str.replace('%','')
  df['Div.Yield'] = df['Div.Yield'].str.replace('.','')
  df['Div.Yield'] = df['Div.Yield'].str.replace(',','.')
  df['Div.Yield'] = pd.to_numeric(df['Div.Yield'])

  df = df.drop(df[df['Volume Financ.(R$)'] < 1000000].index)
  df = df.drop(df[df['Margem EBIT'] < 0].index)
  df = df.drop(df[df['Margem EBIT'].isna()].index)

  df['Ação2'] = df['Ação'].str.replace(r'\d','')
  volume_fin_maxes = df.groupby(['Ação2'])['Volume Financ.(R$)'].transform(max)
  df = df.loc[df['Volume Financ.(R$)'] == volume_fin_maxes]

  df = df.sort_values(by=['EV/EBIT'], ascending=True)
  df = df.reset_index(drop=True)

  acoes_baratas = df[['Ação','Empresa','EV/EBIT','Div.Yield','Volume Financ.(R$)']]
  return acoes_baratas

st.title('Análise de ações')

st.write('Busque os dados pelo site: https://www.investsite.com.br/selecao_acoes.php')
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:

  # Can be used wherever a "file-like" object is accepted:
  dataframe = pd.read_csv(uploaded_file, encoding = "ISO-8859-1", sep=";")
  df = transform_filter_data(dataframe)
  st.write(df.style.hide_index())

  st.sidebar.header('Escolha a ação')

  n_dias = st.slider('Quantidade de dias de previsão', 30, 365)

  acao = df['Empresa']
  nome_acao_escolhida = st.sidebar.selectbox('Escolha uma ação', acao)

  df_acao = df[df['Empresa'] == nome_acao_escolhida]
  acao_escolhida = df_acao.iloc[0]['Ação']
  acao_escolhida = acao_escolhida + '.SA'

  @st.cache
  def pegar_valores_online(sigla_acao):
    df = yf.download(sigla_acao, DATA_INICIO, DATA_FIM)
    df.reset_index(inplace=True)
    return df

  df_valores = pegar_valores_online(acao_escolhida)

  st.subheader('Tabela de valores - ' + nome_acao_escolhida)
  st.write(df_valores.tail(10))

  st.subheader('Grafico de preços')
  fig = go.Figure()
  fig.add_trace(go.Scatter(x=df_valores['Date'],
                            y=df_valores['Close'],
                            name='Preço Fechamento',
                            line_color='yellow'))
  fig.add_trace(go.Scatter(x=df_valores['Date'],
                            y=df_valores['Open'],
                            name='Preço Abertura',
                            line_color='blue'))

  st.plotly_chart(fig)

  df_treino = df_valores[['Date', 'Close']]

  df_treino = df_treino.rename(columns={"Date":'ds', "Close":'y'})

  modelo = Prophet()
  modelo.fit(df_treino)

  futuro = modelo.make_future_dataframe(periods=n_dias, freq='B')
  previsao = modelo.predict(futuro)

  st.subheader('Previsão')
  st.write(previsao[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(n_dias))

  grafico1 = plot_plotly(modelo, previsao)
  st.plotly_chart(grafico1)

  grafico2 = plot_components_plotly(modelo, previsao)
  st.plotly_chart(grafico2)


