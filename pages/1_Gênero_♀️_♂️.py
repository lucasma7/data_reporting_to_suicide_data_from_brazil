import pandas as pd
import plotly.express as px
import streamlit as st


# Configurações iniciais da página
st.set_page_config(page_title="Gênero", layout="wide")

# Obtendo os dados
data_sus = st.session_state.data_sus

sub_col = {"SEXO"       : "Sexo",
           "LOCOCOR"    : "Local de Ocorrência",
           "CAUSABAS_O" : "Suicídios"}

data_sexo = data_sus.groupby("SEXO")["CAUSABAS_O"].count()
data_sexo = data_sexo.reset_index()
data_sexo = data_sexo.rename(columns=sub_col)
data_sexo = data_sexo.sort_values("Suicídios")

data_sexo_local = data_sus[data_sus["SEXO"].isin(["Masculino", "Feminino"])]
data_sexo_local = data_sexo_local.groupby(["SEXO", "LOCOCOR"])["CAUSABAS_O"].count()
data_sexo_local = data_sexo_local.reset_index()
data_sexo_local = data_sexo_local.rename(columns=sub_col)
data_sexo_local = data_sexo_local.sort_values("Suicídios")

total_por_categoria = data_sexo_local.groupby("Sexo")["Suicídios"].transform("sum")
data_sexo_local["Proporção"] = data_sexo_local["Suicídios"] / total_por_categoria

# Sumário inicial dos dados
st.title("♀️ ♂️ Análise por Gênero")
st.markdown("##")

col_esquerda, col_centro, col_direita = st.columns(3)

col_esquerda.markdown("Masculino")
col_centro.markdown("Feminino")
col_direita.markdown("Não declarado")

col_esquerda.markdown(f"## {data_sexo[data_sexo['Sexo'] == 'Masculino']['Suicídios'].iloc[0]}")
col_centro.markdown(f"## {data_sexo[data_sexo['Sexo'] == 'Feminino']['Suicídios'].iloc[0]}")
col_direita.markdown(f"## {data_sexo[data_sexo['Sexo'] == 'Não declarado']['Suicídios'].iloc[0]}")

st.markdown("""---""")

# Exibindo dados

col1, col2 = st.columns((7, 3))
col3, col4 = st.columns((7, 3))

fig1 = px.ecdf(data_sus, x="IDADE", color="SEXO",
               markers=True, lines=False, marginal="histogram",
               title="Distribuição de suicídios por idade e sexo (2012-2020)")
fig1.update_layout(xaxis_title="Idade", yaxis_title="fda")
col1.plotly_chart(fig1, use_container_width=True)

fig2 = px.box(data_sus, x="SEXO", y="IDADE",
              title="Concentração dos casos de suicídio nas idades por sexo (2012-2020)")
fig2.update_xaxes(title="")
fig2.update_yaxes(title="")
col2.plotly_chart(fig2, use_container_width=True)

fig3 = px.bar(data_sexo_local, x="Sexo", y="Proporção", color="Local de Ocorrência",
              title="Proporção de suicídios por local de ocorrência com relação ao sexo (2012-2020)")
fig3.update_xaxes(title="")
fig3.update_yaxes(title="")
fig3.update_layout(barmode="group")
col3.plotly_chart(fig3, use_container_width=True)

fig4 = px.pie(names=data_sexo["Sexo"], values=data_sexo["Suicídios"], hole=.7,
              title="Ocorrências de suicídio por sexo (2012-2020)")
col4.plotly_chart(fig4, use_container_width=True)
