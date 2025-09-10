import streamlit as st
import pandas as pd
import yfinance as yf
import datetime as dt   

#criar funções de carregamento de dados
@st.cache_data
def carregar_dados(empresas):
    texto_stickers =  " ".join(empresas) 
    dados_acao = yf.Tickers(texto_stickers)
    cotacoes_acao = dados_acao.history(period="14y", start="2010-01-01")
    cotacoes_acao = cotacoes_acao["Close"]
    return cotacoes_acao

acoes = ["ITUB4.SA", "PETR4.SA", "MGLU3.SA", "VALE3.SA", "ABEV3.SA", "GGBR4.SA"]
dados = carregar_dados(acoes)  
   

# "ITUB4.SA" pega o codigo do banco "ticker". Para o brasil, "CÓD + SA"=bolsa de sao paulo.  
# cotacao das ações ao longo de 2010 a 2024

#cria a interface do streamlit
st.write("""
# App Preço de Ações Itaú 
O gráfico abaixo representa a evolução do preço das ações do Itaú (ITUB4), ao  longo dos anos
""") # markdown

#FILTROS - preparação das visualizações 

st.sidebar.header("Filtros") #titulo da sidebar

#filtro de ações
lista_acoes = st.sidebar.multiselect("Escolha qual ou quais ações para visualizar:", dados.columns)
if lista_acoes:
    dados=dados[lista_acoes]
    if len(lista_acoes)==1:
        acao_unica = lista_acoes[0]
        dados=dados.rename(columns={acao_unica: "Close"})

#filtro de datas
data_inicial = dados.index.min().to_pydatetime()
data_final = dados.index.max().to_pydatetime()
intervalo_data = st.sidebar.slider("Selecione o período desejado",
                                   min_value=data_inicial,
                                   max_value=data_final,
                                   value=(data_inicial, data_inicial),
                                   step=dt.timedelta(days=1))
dados = dados.loc[intervalo_data[0]:intervalo_data[1]]

#cria o grafico
st.line_chart(dados, y_label="R$")

#st.write("""
# Fim do App
#""")

