from dash import Dash, dcc, html, Input, Output
from matplotlib.pyplot import xticks
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

BS = "./bootstrap.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])

templates = [
    "bootstrap",
    "minty",
    "pulse",
    "flatly",
    "quartz",
    "cyborg",
    "darkly",
    "vapor",
]

load_figure_template(templates)

df = pd.read_csv('./cota-parlamentar.csv')

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

dict = {1:'Janeiro', 2:'Fevereiro', 3:'Março', 4:'Abril', 5:'Maio', 6:'Junho', 7:'Julho', 8:'Agosto', 9:'Setembro', 10:'Outubro', 11:'Novembro', 12:'Dezembro'}
df.replace({"Mês": dict}, inplace=True)

group_valor_partido = df.groupby(['Partido', 'Mês', 'Ano'])[['Valor Líquido']].sum('Valor Líquido').reset_index()

group_valor_descricao = df.groupby(['Descrição', 'Partido', 'Ano'])[['Valor Líquido']].sum('Valor Líquido').reset_index()


header = html.H4(
    "Gastos dos partidos políticos", className="bg-primary text-white my-2 text-center"
)

valor_partido = group_valor_partido[(group_valor_partido['Partido'] == 'PT') & (group_valor_partido['Ano'] == 2020)]
valor_descricao = group_valor_descricao[(group_valor_descricao['Partido'] == 'PT') & (group_valor_descricao['Ano'] == 2020)]

fig = px.bar(valor_partido, x="Mês", y="Valor Líquido", barmode="group", title="Gasto Mensal", color="Mês", text='Valor Líquido', template="vapor")
fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
fig.update_yaxes(visible=False, showticklabels=False)


fig2 = px.bar(valor_descricao, y="Descrição", x="Valor Líquido", barmode="group", title="Gastos por Categoria", orientation='h', text='Valor Líquido', template="vapor")
fig2.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
fig2.update_xaxes(visible=False, showticklabels=False)
fig2.update_yaxes(ticklabelposition="inside top", title=None)


partidos = df['Partido'].unique()

input_partido = dcc.Dropdown(options = [
                        {'label': 'PSDB', 'value': 'PSDB'},
                        {'label': 'PT', 'value': 'PT'},
                        {'label': 'PSL', 'value': 'PSL'},
                        {'label': 'NOVO', 'value': 'NOVO'},
                        {'label': 'PDT', 'value': 'PDT'}], value='PT', id='partidos-dropdown')
input_ano = dcc.Dropdown(options= [
                        {'label': '2014', 'value': 2014},
                        {'label': '2015', 'value': 2015},
                        {'label': '2016', 'value': 2016},
                        {'label': '2017', 'value': 2017},
                        {'label': '2018', 'value': 2018},
                        {'label': '2019', 'value': 2019},
                        {'label': '2020', 'value': 2020}], value=2020, id='ano-dropdown')

graph = html.Div(dcc.Graph(id="graph", figure=fig), className="mx-auto")
graph2 = html.Div(dcc.Graph(id="graph2", figure=fig2), className="mx-auto")


app.layout = dbc.Container(
    [
        header,
        dbc.Row(
            [
                dbc.Col([input_partido, "Selecione um partido", input_ano, "Selecione um ano"],width=10, className="card border-primary rounded mx-auto p-2"),
            ]
        ),
        dbc.Row(
            [
                dbc.Col([graph],width=10, className="card border-secondary rounded mx-auto my-2 p-2"),
                dbc.Col([graph2],width=10, className="card border-info rounded mx-auto my-2 p-2"),
            ]
        ),
    ],
    className="dbc",
    fluid=True
)

@app.callback(
    [
        Output("graph", "figure"),
        Output("graph2", "figure"),
    ],
    [
        Input("partidos-dropdown", "value"),
        Input("ano-dropdown", "value"),
    ],
)
def chem_info_on_hover(partido_hoverData, ano_hoverData):
    valor_partido = group_valor_partido[(group_valor_partido['Partido'] == partido_hoverData) & (group_valor_partido['Ano'] == ano_hoverData)]
    valor_descricao = group_valor_descricao[(group_valor_descricao['Partido'] == partido_hoverData) & (group_valor_descricao['Ano'] == ano_hoverData)]

    fig = px.bar(valor_partido, x="Mês", y="Valor Líquido", barmode="group", title="Gasto Mensal", text='Valor Líquido', template="vapor")
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.update_yaxes(visible=False, showticklabels=False)

    fig2 = px.bar(valor_descricao, y="Descrição", x="Valor Líquido", barmode="group", title="Gastos por Categoria", orientation='h', text='Valor Líquido', template="vapor")
    fig2.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig2.update_xaxes(visible=False, showticklabels=False)
    fig2.update_yaxes(ticklabelposition="inside top", title=None)

    return (fig, fig2)


if __name__ == "__main__":
    app.run_server(debug=True)