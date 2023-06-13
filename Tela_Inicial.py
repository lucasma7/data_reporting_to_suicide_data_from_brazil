import json
import pandas as pd
import plotly.express as px
import streamlit as st


# Configurações iniciais da página
st.set_page_config(page_title="Observatório de Dados", layout="wide", initial_sidebar_state="expanded")

# Carregando dados que serão utilizados no app
st.session_state.data_sus = pd.read_csv("dados/data_suicide.csv")
st.session_state.geojson  = json.load(open("dados/brasil_estados.json"))

# Obtendo os dados
data_sus, geojson = st.session_state.data_sus, st.session_state.geojson

data_estado = data_sus.groupby("ESTADO").count()
data_estado = data_estado.reset_index()[["ESTADO", "CAUSABAS"]]
data_estado = data_estado.rename(columns={"ESTADO" : "Estado", "CAUSABAS" : "Suicídios"})
data_estado = data_estado.sort_values("Suicídios")

data_estado_10 = data_estado.iloc[-10:]

# Cabeçalho inicial
# Sumário de informações relevantes
st.markdown("<h1 style='text-align: center'>Observatório de Dados sobre o Suicídio</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

fig1 = px.choropleth(data_estado, geojson=geojson, locations="Estado",
                     color="Suicídios", scope="south america")
fig1.update_geos(showcountries=False, fitbounds="locations")
col1.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(data_estado_10, x="Suicídios", y="Estado", text="Suicídios")
fig2.update_xaxes(title="", showticklabels=False)
fig2.update_yaxes(title="", tickmode="linear")
col2.plotly_chart(fig2, use_container_width=True)

# Mais informações sobre o projeto
with st.expander("Mais informações"):
    st.caption("Registros de suicídio no Brasil entre os anos de 2012 e 2020 informados pelo SUS. "
               "Dados brutos disponíveis na página do [DATASUS](https://datasus.saude.gov.br/).")
