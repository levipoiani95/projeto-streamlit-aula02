import streamlit as st
import pandas as pd
import yfinance as yf
import datetime as dt
import math

#criar funções de carregamento de dados
@st.cache_data
def carregar_dados(empresas):
    texto_stickers =  " ".join(empresas) 
    dados_acao = yf.Tickers(texto_stickers)
    cotacoes_acao = dados_acao.history(period="14y", start="2010-01-01")
    cotacoes_acao = cotacoes_acao["Close"]
    return cotacoes_acao

@st.cache_data
def carregar_tickers_acoes():
    base_tickers = pd.read_csv("IBOV.csv", sep=";")
    tickers = list(base_tickers["Código"])
    tickers = [item + ".SA" for item in tickers] # pra cada item dentro tickers, seja armazenado com .SA
    return tickers

acoes = carregar_tickers_acoes() 
dados = carregar_dados(acoes)  
   

# "ITUB4.SA" pega o codigo do banco "ticker". Para o brasil, "CÓD + SA"=bolsa de sao paulo.  
# cotacao das ações ao longo de 2010 a 2024

#cria a interface do streamlit
st.write("""
###### Desenvolvida por Levi Poiani e no Curso Hashtag Streamlit com Python     
# Bem-vindo! 
### Essa é a Dashboard Preço de Ações do Brasil 
         
O gráfico abaixo representa a o comportamento do preço das **ações brasileiras de 2010 a 2024** 
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

#Calculo performance da carteira
texto_performance_ativos = ""

if len(lista_acoes)==0:
    lista_acoes = list(dados.columns)
elif len(lista_acoes)==1:
    dados=dados.rename(columns={"Close":acao_unica})

carteira = [1 for acao in lista_acoes] #pra cada acao da carteira, tenho 1000 reais 
total_inicial_carteira = sum(carteira)  


for i, acao in enumerate(lista_acoes):    
    performance_ativo = dados[acao].iloc[-1]/ dados[acao].iloc[0] -1
    performance_ativo = float(performance_ativo)
    carteira[i]= (1 + performance_ativo) * carteira[i]  
    

    if math.isnan(performance_ativo):
    #No markdown texto eh pintado: :cor[texto]
        texto_performance_ativos = texto_performance_ativos + f"  \n{acao} : :gray[Não existe nesse período]"

    if performance_ativo > 0:
    #No markdown texto eh pintado: :cor[texto]
        texto_performance_ativos = texto_performance_ativos + f"  \n{acao} : :green[{performance_ativo:.1%}]"
    elif performance_ativo < 0:
        texto_performance_ativos = texto_performance_ativos + f"  \n{acao} : :red[{performance_ativo:.1%}]"
    elif performance_ativo == 0:
        texto_performance_ativos = texto_performance_ativos + f"  \n{acao} : :yellow[{performance_ativo:.1%}]"
    #else:
    #   texto_performance_ativos = texto_performance_ativos + f"  \n{acao} : :blue[{performance_ativo:.1%}]"

total_final_carteira = sum(carteira)
perfomance_carteira = total_final_carteira/total_inicial_carteira-1

if perfomance_carteira > 0:
    texto_perfomance_carteira = f"Performance da carteira com todos os ativos : :green[{perfomance_carteira:.1%}]"
elif perfomance_carteira < 0:
    texto_perfomance_carteira = f"Performance da carteira com todos os ativos : :red[{perfomance_carteira:.1%}]"
elif perfomance_carteira == 0:
    texto_perfomance_carteira = f"Performance da carteira com todos os ativos : :blue[{perfomance_carteira:.1%}]"
else:
    texto_perfomance_carteira = f"Performance da carteira com todos os ativos : :gray[{perfomance_carteira:.1%}]"
    

st.write(f"""
## Performance dos Ativos
Essa foi a perfomance de cada ativo no período selecionado:

{texto_performance_ativos}         
{texto_perfomance_carteira}
""")

