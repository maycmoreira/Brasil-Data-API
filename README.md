# Brasil Data API 🇧🇷

Uma API RESTful completa para análise de dados demográficos e econômicos brasileiros, com processamento de dados em tempo real, análise estatística e visualizações interativas.

## 🚀 Funcionalidades

- **API RESTful** desenvolvida com Flask & Flask-RESTX
- **Dashboard Interativo** com Streamlit & Plotly
- **Análise Estatística** (correlações, tendências, distribuições)
- **Visualização de Dados** com gráficos interativos
- **Documentação Automática** com Swagger/OpenAPI
- **CORS Habilitado** para requisições cross-origin

## 📊 Análises de Dados Incluídas

- **Análise Populacional** por estado e região
- **Ranking de PIB** dos municípios brasileiros
- **Indicadores de IDH** e correlações
- **Distribuição Regional** pelas 5 regiões do Brasil
- **Correlações Econômicas** entre PIB e indicadores de desenvolvimento
- **Estatísticas Descritivas** para todos os conjuntos de dados

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3** - Linguagem de programação principal
- **Flask** - Framework web
- **Flask-RESTX** - Desenvolvimento de API com documentação Swagger
- **Flask-CORS** - Compartilhamento de recursos entre origens

### Data Science
- **Pandas** - Manipulação e análise de dados
- **NumPy** - Computação numérica
- **Matplotlib** - Visualização de dados

### Frontend & Visualização
- **Streamlit** - Dashboard web interativo
- **Plotly** - Gráficos e visualizações interativas

## 📈 Endpoints da API

### Estados e Regiões
- `GET /estados/` - Lista todos os estados brasileiros
- `GET /estados/{sigla}` - Dados de um estado específico
- `GET /analise/estados-comparacao` - Comparação entre estados

### Dados Municipais
- `GET /municipios/pib` - PIB dos municípios
- `GET /municipios/idh` - IDH dos municípios
- `GET /analise/ranking-pib` - Ranking de municípios por PIB

### Análises Estatísticas
- `GET /analise/correlacao-pib-idh` - Correlação entre PIB e IDH
- `GET /analise/distribuicao-regional` - Distribuição regional
- `GET /analise/estatisticas-pib` - Estatísticas descritivas do PIB
- `GET /analise/populacao-total` - Análise da população total
