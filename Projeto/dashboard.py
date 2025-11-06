import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(
    page_title="Dashboard IBGE",
    page_icon="📊",
    layout="wide"
)

# Título
st.title("📊 Dashboard - Dados IBGE API")
st.markdown("Análise de dados demográficos e econômicos em tempo real")

# URL da API
API_URL = "http://localhost:5000"

@st.cache_data(ttl=300)
def carregar_dados(endpoint):
    """Carrega dados da API"""
    try:
        response = requests.get(f"{API_URL}{endpoint}", timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

# Sidebar
st.sidebar.title("Configurações")
opcao = st.sidebar.selectbox(
    "Selecione a análise:",
    ["Estados", "Municípios", "Ranking PIB", "Comparação Regional"]
)

if opcao == "Estados":
    st.header("🏢 Dados por Estado")
    
    dados_estados = carregar_dados("/estados/")
    if dados_estados:
        df_estados = pd.DataFrame(dados_estados['estados'])
        st.dataframe(df_estados[['nome', 'sigla', 'regiao']].head(10))
        
        # Gráfico de estados por região
        contagem_regiao = df_estados['regiao'].value_counts()
        fig = px.bar(contagem_regiao, title="Estados por Região")
        st.plotly_chart(fig)

elif opcao == "Municípios":
    st.header("🏘️ Dados por Município")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("PIB Municipal")
        dados_pib = carregar_dados("/municipios/pib")
        if dados_pib:
            st.metric("Municípios com dados", dados_pib['total_municipios'])
    
    with col2:
        st.subheader("IDH Municipal")
        dados_idh = carregar_dados("/municipios/idh")
        if dados_idh:
            st.metric("Municípios com dados", dados_idh['total_municipios'])

elif opcao == "Ranking PIB":
    st.header("💰 Ranking PIB Municipal")
    
    dados_ranking = carregar_dados("/analise/ranking-pib")
    if dados_ranking:
        df_ranking = pd.DataFrame(dados_ranking['ranking'])
        st.dataframe(df_ranking.head(10))
        
        # Gráfico do top 10
        if len(df_ranking) > 0:
            fig = px.bar(df_ranking.head(10), 
                        x='municipio', y='pib',
                        title="Top 10 Municípios por PIB")
            st.plotly_chart(fig)

elif opcao == "Comparação Regional":
    st.header("🗺️ Comparação Regional")
    
    dados_distribuicao = carregar_dados("/analise/distribuicao-regional")
    if dados_distribuicao:
        df_distribuicao = pd.DataFrame(dados_distribuicao['distribuicao']).T.reset_index()
        df_distribuicao.columns = ['Região', 'Estados', 'População', 'PIB per capita', 'IDH']
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.bar(df_distribuicao, x='Região', y='População',
                         title="População por Região")
            st.plotly_chart(fig1)
        
        with col2:
            fig2 = px.bar(df_distribuicao, x='Região', y='PIB per capita',
                         title="PIB per Capita por Região")
            st.plotly_chart(fig2)

# Status da API
st.sidebar.markdown("---")
st.sidebar.subheader("Status da API")
health = carregar_dados("/health")
if health:
    st.sidebar.success("✅ API Online")
else:
    st.sidebar.error("❌ API Offline")

st.markdown("---")
st.markdown("**📊 Dashboard criado com dados da API IBGE**")