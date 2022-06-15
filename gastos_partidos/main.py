import pandas as pd
from plotnine import ggplot, aes, geom_line, facet_grid
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
sns.set_theme(style="ticks", color_codes=True)

df = pd.read_csv('./cota-parlamentar.csv')

df.head()

df.rename({
'numano'	:	'Ano',
'nummes'	:	'Mês',
'datemissao'	:	'Data da Emissão',
'txnomeparlamentar'	:	'Parlamentar'	,
'sgpartido'	:	'Partido'	,
'sguf'	:	'UF'	,
'txtdescricao'	:	'Descrição'	,
'txtcnpjcpf'	:	'CPF/CNPJ do Fornecedor'	,
'txtfornecedor'	:	'Fornecedor'	,
'vlrdocumento'	:	'Valor do Documento'	,
'vlrglosa'	:	'Valor Glosa'	,
'codlegislatura'	:	'codlegislatura'	,
'vlrliquido'	:	'Valor Líquido'	,
'idedocumento'	:	'idedocumento'	,
'idecadastro'	:	'idecadastro'	,
'indtipodocumento'	:	'indtipodocumento'	,
'nucarteiraparlamentar'	:	'nucarteiraparlamentar'	,
'nudeputadoid'	:	'nudeputadoid'	,
'nulegislatura'	:	'nulegislatura'	,
'numespecificacaosubcota'	:	'numespecificacaosubcota'	,
'numlote'	:	'numlote'	,
'numparcela'	:	'numparcela'	,
'numressarcimento'	:	'numressarcimento'	,
'numsubcota'	:	'numsubcota'	,
'txtdescricaoespecificacao'	:	'txtdescricaoespecificacao'	,
'txtnumero'	:	'txtnumero'	,
'txtpassageiro'	:	'Passageiro'	,
'txttrecho'	:	'Trecho'	,
'vlrrestituicao':'Valor da Restituição'
}, axis=1, inplace=True)

df.head()

df[df['Partido'].isin(['PSDB', 'PT', 'NOVO', 'PDT', 'PODE', 'PP', 'PSD',
       'PTB', 'DEM', 'PSB', 'REPUBLICANOS', 'CIDADANIA', 'PSOL',
       'MDB', 'PCdoB', 'PL', 'PSC', 'PSL'])]


group_valor_partido = df.groupby(['Mês', 'Ano', 'Partido'])[['Valor Líquido']].sum('Valor Líquido').reset_index()

group_valor_partido[group_valor_partido['Partido'] == 'PT']

sns.barplot(x="Partido", y="Valor Líquido", hue="Mês", palette="ch:.25", data=group_valor_partido[group_valor_partido['Partido'] == 'PT'])


group_valor_descricao = df.groupby(['Descrição', 'Ano', 'Partido'])[['Valor Líquido']].sum('Valor Líquido').reset_index()

group_valor_descricao[(group_valor_descricao['Partido'] == 'PT') & (group_valor_descricao['Ano'] == 2020)].head()

group_valor_descricao.head()


import plotly.express as px

fig = px.bar(group_valor_partido[(group_valor_partido['Partido'] == 'PT') & (group_valor_partido['Ano'] == 2020)], x="Mês", y="Valor Líquido", barmode="group", title="Gastos Mensal", color="Mês")
fig.update_xaxes(visible=False, showticklabels=False)
fig



fig2 = px.bar(group_valor_descricao[(group_valor_descricao['Partido'] == 'PT') & (group_valor_descricao['Ano'] == 2020)], y="Descrição", x="Valor Líquido", barmode="group", title="Gastos por Categoria", orientation='h')
fig2.update_xaxes(visible=False, showticklabels=False)
fig2.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
))

fig2.show()
