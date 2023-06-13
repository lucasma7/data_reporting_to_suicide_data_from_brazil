import pandas as pd
import plotly.express as px
import streamlit as st


# Configurações iniciais da página
st.set_page_config(page_title="Características do Óbito", layout="wide")

# Definindo constantes
cod_cid10 = {
    "X700" : "Enforcamento e estrangulamento",
    "X709" : "Método de suicídio não especificado",
    "X708" : "Outros métodos de suicídio não especificados",
    "X740" : "Explosão de gás doméstico",
    "X704" : "Incêndio",
    "X680" : "Envenenamento e exposição a substâncias nocivas",
    "X689" : "Método de suicídio não especificado",
    "X720" : "Uso de arma de fogo não especificada",
    "X701" : "Envenenamento acidental não especificado",
    "X800" : "Ferimento autoprovocado por arma cortante",
    "X749" : "Método de suicídio não especificado",
    "X707" : "Asfixia acidental não especificada",
    "X699" : "Método de suicídio não especificado",
    "X640" : "Envenenamento e exposição a substâncias nocivas",
    "X610" : "Salto ou pendente de altura",
    "X649" : "Método de suicídio não especificado",
    "X780" : "Método de suicídio não especificado",
    "X690" : "Envenenamento e exposição a substâncias nocivas",
    "X849" : "Método de suicídio não especificado",
    "X804" : "Ferimento autoprovocado com objetos afiados não cortantes"
}

df_cid10 = pd.DataFrame(list(cod_cid10.items()),
                        columns=["cid-10", "Descrição"])

sub_col = {"LOCOCOR"    : "Local de ocorrência",
           "FONTE"      : "Fonte",
           "CAUSABAS_O" : "Suicídios",
           "count"      : "Suicídios"}

# Obtendo os dados
data_sus = st.session_state.data_sus

data_lococor = data_sus.groupby("LOCOCOR")["CAUSABAS_O"].count()
data_lococor = data_lococor.reset_index()
data_lococor = data_lococor.rename(columns=sub_col)
data_lococor = data_lococor.sort_values("Suicídios")

data_fonte = data_sus.groupby("FONTE")["CAUSABAS_O"].count()
data_fonte = data_fonte.reset_index()
data_fonte = data_fonte.rename(columns=sub_col)
data_fonte = data_fonte.sort_values("Suicídios")

data_sus["CAUSABAS"] = data_sus.CAUSABAS.str.strip()
data_sus["CAUSABAS_O"] = data_sus.CAUSABAS_O.str.strip()

df_causas = data_sus.CAUSABAS.value_counts()[:20]
df_causas = pd.DataFrame(df_causas).merge(df_cid10, left_index=True, right_on="cid-10")
df_causas = df_causas.rename(columns=sub_col)

df_causas = df_causas[["Suicídios", "Descrição"]].groupby("Descrição").sum()
df_causas = df_causas.sort_values(by=["Suicídios"])
df_causas = df_causas.reset_index()

# Sumário inicial dos dados
st.title("Análise por Características do Óbito")
st.markdown("##")

col_esquerda, col_centro, col_direita = st.columns(3)

col_esquerda.markdown("Domicílio")
col_centro.markdown("Ocorrência Policial")
col_direita.markdown("Enforcamento e estrangulamento")

col_esquerda.markdown(f"## {data_lococor[data_lococor['Local de ocorrência'] == 'domicílio']['Suicídios'].iloc[0]}")
col_centro.markdown(f"## {data_fonte[data_fonte['Fonte'] == 'Ocorrência Policial']['Suicídios'].iloc[0]}")
col_direita.markdown(f"## {df_causas[df_causas['Descrição'] == 'Enforcamento e estrangulamento']['Suicídios'].iloc[0]}")

st.markdown("""---""")

# Exibindo dados

col1, col2 = st.columns(2)

fig1 = px.bar(data_lococor, x="Local de ocorrência", y="Suicídios", text="Suicídios",
              title="Ocorrências de suicídio com relação ao local de ocorrência (2012-2020)")
fig1.update_xaxes(title="")
fig1.update_yaxes(title="", showticklabels=False)
col1.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(data_fonte, x="Fonte", y="Suicídios", text="Suicídios",
              title="Ocorrências de suicídio com relação à fonte (2012-2020)")
fig2.update_xaxes(title="")
fig2.update_yaxes(title="", showticklabels=False)
col2.plotly_chart(fig2, use_container_width=True)

fig3 = px.bar(df_causas, x="Suicídios", y="Descrição", text="Suicídios",
              title="Distribuição das descrições do suicídio")
fig3.update_xaxes(title="", showticklabels=False)
fig3.update_yaxes(title="", tickmode="linear")
st.plotly_chart(fig3, use_container_width=True)
