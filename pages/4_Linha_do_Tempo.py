import pandas as pd
import plotly.express as px
import streamlit as st
from statsmodels.tsa.seasonal import seasonal_decompose


# Configurações iniciais da página
st.set_page_config(page_title="Série Temporal", layout="wide")

# Obtendo os dados
data_sus = st.session_state.data_sus
data_sus["DTOBITO"] = pd.to_datetime(data_sus["DTOBITO"], format="%Y-%m-%d")

sub_col = {"DTOBITO"  : "Ano",
           "CAUSABAS" : "Suicídios"}

data_year_month = data_sus.groupby([data_sus["DTOBITO"].dt.year, data_sus["DTOBITO"].dt.month]).count()
data_year_month = data_year_month[["CAUSABAS"]].rename(columns=sub_col)
data_year_month["Mês"] = ["/".join(str(v) for v in year_month)
                          for year_month in data_year_month.index]

data_dtobito = data_sus.groupby(data_sus["DTOBITO"].dt.year).count()["CAUSABAS"]
data_dtobito = data_dtobito.reset_index()
data_dtobito = data_dtobito.rename(columns=sub_col)

decomposition = seasonal_decompose(data_year_month["Suicídios"], period=12)
data_year_month["Tendência"] = decomposition.trend
data_year_month["Sazonalidade"] = decomposition.seasonal

data_dtobito_menor = data_sus[data_sus["IDADE"] < 18]
data_dtobito_menor = data_dtobito_menor.groupby(data_sus["DTOBITO"].dt.year).count()["CAUSABAS"]
data_dtobito_menor = data_dtobito_menor.reset_index()
data_dtobito_menor = data_dtobito_menor.rename(columns=sub_col)

data_dtobito_menor = data_sus[data_sus["IDADE"] < 18]
data_dtobito_menor = data_dtobito_menor.groupby(data_sus["DTOBITO"].dt.year).count()["CAUSABAS"]
data_dtobito_menor = data_dtobito_menor.reset_index()
data_dtobito_menor = data_dtobito_menor.rename(columns=sub_col)

months = ["January", "February", "March",
          "April", "May", "June",
          "July", "August", "September",
          "October", "November", "December"]

data_2020 = data_sus[data_sus["DTOBITO"].dt.year == 2020]
data_2020 = data_2020.groupby(data_sus["DTOBITO"].dt.month).count()
data_2020 = data_2020['CAUSABAS'].reset_index()
data_2020 = data_2020.rename(columns={'DTOBITO' : 'Mês', 'CAUSABAS' : 'Suicídios'})
data_2020["Mês"] = months

# Sumário inicial dos dados
st.title("Análise por Séries Temporais")
st.markdown("""---""")

# Exibindo dados

fig0 = px.line(data_year_month, x="Mês", y="Suicídios",
               title="Ocorrências de suicídio por mês (2012-2020)")
fig0.update_xaxes(tickmode="array",
                  tickvals=data_year_month["Mês"][::6],
                  ticktext=data_year_month["Mês"][::6],
                  title="")
fig0.update_yaxes(title="")
st.plotly_chart(fig0, use_container_width=True)

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

fig1 = px.line(data_dtobito, x="Ano", y="Suicídios",
               title="Ocorrências de suicídio por ano (2012-2020)")
fig1.update_xaxes(title="")
fig1.update_yaxes(title="")
col1.plotly_chart(fig1, use_container_width=True)

fig2 = px.line(data_year_month, x="Mês", y=["Tendência", "Sazonalidade"],
               title="Tendência e sazonalidade das ocorrências de suicídio por mês (2012-2020)")
fig2.update_xaxes(tickmode="array",
                  tickvals=data_year_month["Mês"][::6],
                  ticktext=data_year_month["Mês"][::6],
                  title="")
fig2.update_yaxes(title="")
col2.plotly_chart(fig2, use_container_width=True)

fig3 = px.line(data_dtobito_menor, x="Ano", y="Suicídios",
               title="Ocorrências de suicídio entre menores por ano (2012-2020)")
fig3.update_xaxes(title="")
fig3.update_yaxes(title="")
col3.plotly_chart(fig3, use_container_width=True)

fig4 = px.line(data_2020, x="Mês", y="Suicídios",
               title="Ocorrências de suicídio por mês (2020)")
fig4.update_xaxes(title="")
fig4.update_yaxes(title="")
col4.plotly_chart(fig4, use_container_width=True)
