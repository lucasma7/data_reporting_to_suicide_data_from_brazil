import pandas as pd
import plotly.express as px
import streamlit as st


# Configurações iniciais da página
st.set_page_config(page_title="Características Pessoais", layout="wide")

# Obtendo os dados
data_sus = st.session_state.data_sus

sub_col = {"RACACOR"    : "Raça/Cor",
           "ESTCIV"     : "Estado Civil",
           "ESC"        : "Escolaridade",
           "CAUSABAS_O" : "Suicídios"}

data_racacor = data_sus.groupby("RACACOR")["CAUSABAS_O"].count()
data_racacor = data_racacor.reset_index()
data_racacor = data_racacor.rename(columns=sub_col)
data_racacor = data_racacor.sort_values("Suicídios")

data_estciv = data_sus.groupby("ESTCIV")["CAUSABAS_O"].count()
data_estciv = data_estciv.reset_index()
data_estciv = data_estciv.rename(columns=sub_col)
data_estciv = data_estciv.sort_values("Suicídios")

data_esc = data_sus.groupby("ESC")["CAUSABAS_O"].count()
data_esc = data_esc.reset_index()
data_esc = data_esc.rename(columns=sub_col)
data_esc = data_esc.sort_values("Suicídios")

# Sumário inicial dos dados
st.title("Análise por Características Pessoais")
st.markdown("##")

col_esquerda, col_centro, col_direita = st.columns(3)

col_esquerda.markdown("Parda")
col_centro.markdown("Solteiro")
col_direita.markdown("Ensino Médio")

col_esquerda.markdown(f"## {data_racacor[data_racacor['Raça/Cor'] == 'Parda']['Suicídios'].iloc[0]}")
col_centro.markdown(f"## {data_estciv[data_estciv['Estado Civil'] == 'Solteiro']['Suicídios'].iloc[0]}")
col_direita.markdown(f"## {data_esc[data_esc['Escolaridade'] == 'Médio']['Suicídios'].iloc[0]}")

st.markdown("""---""")


# Exibindo dados

fig0 = px.bar(data_racacor, x="Raça/Cor", y="Suicídios", text="Suicídios",
              title="Ocorrências de suicídio por raça/cor (2012-2020)")
fig0.update_xaxes(title="")
fig0.update_yaxes(title="", showticklabels=False)
st.plotly_chart(fig0, use_container_width=True)

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

fig1 = px.bar(data_estciv, x="Estado Civil", y="Suicídios", text="Suicídios",
              title="Ocorrências de suicídio por estado civil (2012-2020)")
fig1.update_xaxes(title="")
fig1.update_yaxes(title="", showticklabels=False)
col1.plotly_chart(fig1, use_container_width=True)

fig2 = px.box(data_sus, x="ESTCIV", y="IDADE",
              title="Concentração dos casos de suicídio nas idades por estado civil (2012-2020)")
fig2.update_xaxes(title="")
fig2.update_yaxes(title="")
col2.plotly_chart(fig2, use_container_width=True)

fig3 = px.bar(data_esc, x="Escolaridade", y="Suicídios", text="Suicídios",
              title="Ocorrências de suicídio com relação à escolaridade (2012-2020)")
fig3.update_xaxes(title="")
fig3.update_yaxes(title="", showticklabels=False)
col3.plotly_chart(fig3, use_container_width=True)

fig4 = px.box(data_sus, x="ESC", y="IDADE",
              title="Concentração dos casos de suicídio nas idades por escolaridade (2012-2020)")
fig4.update_xaxes(title="")
fig4.update_yaxes(title="")
col4.plotly_chart(fig4, use_container_width=True)
