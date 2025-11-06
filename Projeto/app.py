from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restx import Api, Resource, fields
import pandas as pd
import numpy as np
from datetime import datetime

app = Flask(__name__)
CORS(app)
api = Api(app, 
          version='1.0', 
          title='API Análise Dados IBGE',
          description='API para análise de dados demográficos e econômicos do IBGE',
          doc='/docs')

# Dados de exemplo REALISTAS
dados_estados = [
    {'id': '35', 'sigla': 'SP', 'nome': 'São Paulo', 'regiao': {'nome': 'Sudeste'}, 'populacao': 46289333},
    {'id': '33', 'sigla': 'RJ', 'nome': 'Rio de Janeiro', 'regiao': {'nome': 'Sudeste'}, 'populacao': 17463349},
    {'id': '31', 'sigla': 'MG', 'nome': 'Minas Gerais', 'regiao': {'nome': 'Sudeste'}, 'populacao': 21411923},
    {'id': '53', 'sigla': 'DF', 'nome': 'Distrito Federal', 'regiao': {'nome': 'Centro-Oeste'}, 'populacao': 3094323},
    {'id': '29', 'sigla': 'BA', 'nome': 'Bahia', 'regiao': {'nome': 'Nordeste'}, 'populacao': 14985284},
    {'id': '23', 'sigla': 'CE', 'nome': 'Ceará', 'regiao': {'nome': 'Nordeste'}, 'populacao': 9240580},
    {'id': '43', 'sigla': 'RS', 'nome': 'Rio Grande do Sul', 'regiao': {'nome': 'Sul'}, 'populacao': 11422973},
    {'id': '42', 'sigla': 'SC', 'nome': 'Santa Catarina', 'regiao': {'nome': 'Sul'}, 'populacao': 7338473},
    {'id': '41', 'sigla': 'PR', 'nome': 'Paraná', 'regiao': {'nome': 'Sul'}, 'populacao': 11516840},
    {'id': '15', 'sigla': 'PA', 'nome': 'Pará', 'regiao': {'nome': 'Norte'}, 'populacao': 8777124}
]

# Dados realistas de PIB e IDH
dados_pib_idh = [
    {'municipio': 'São Paulo', 'estado': 'SP', 'pib': 699.28, 'idh': 0.805},
    {'municipio': 'Rio de Janeiro', 'estado': 'RJ', 'pib': 344.48, 'idh': 0.799},
    {'municipio': 'Brasília', 'estado': 'DF', 'pib': 254.83, 'idh': 0.824},
    {'municipio': 'Belo Horizonte', 'estado': 'MG', 'pib': 93.44, 'idh': 0.810},
    {'municipio': 'Porto Alegre', 'estado': 'RS', 'pib': 87.21, 'idh': 0.805},
    {'municipio': 'Curitiba', 'estado': 'PR', 'pib': 79.35, 'idh': 0.823},
    {'municipio': 'Fortaleza', 'estado': 'CE', 'pib': 65.12, 'idh': 0.754},
    {'municipio': 'Salvador', 'estado': 'BA', 'pib': 63.45, 'idh': 0.759},
    {'municipio': 'Recife', 'estado': 'PE', 'pib': 58.67, 'idh': 0.772},
    {'municipio': 'Goiânia', 'estado': 'GO', 'pib': 52.34, 'idh': 0.799},
    {'municipio': 'Manaus', 'estado': 'AM', 'pib': 89.52, 'idh': 0.737},
    {'municipio': 'Belém', 'estado': 'PA', 'pib': 42.18, 'idh': 0.746},
    {'municipio': 'Campinas', 'estado': 'SP', 'pib': 68.45, 'idh': 0.805},
    {'municipio': 'São Luís', 'estado': 'MA', 'pib': 35.67, 'idh': 0.768},
    {'municipio': 'Maceió', 'estado': 'AL', 'pib': 28.91, 'idh': 0.721}
]

# Namespaces
ns_estados = api.namespace('estados', description='Dados por estado')
ns_municipios = api.namespace('municipios', description='Dados por município')
ns_analise = api.namespace('analise', description='Análises comparativas')

# Modelos para documentação
filtro_model = api.model('Filtro', {
    'estado_id': fields.String(description='ID do estado'),
    'ano': fields.Integer(description='Ano de referência')
})

class AnaliseDemografica:
    def __init__(self):
        pass
    
    def criar_ranking_pib(self, pib_data):
        """Cria ranking de municípios por PIB"""
        if not pib_data:
            return []
        
        df = pd.DataFrame(pib_data)
        
        # Ordena por PIB em ordem decrescente
        if 'pib' in df.columns:
            df_sorted = df.sort_values('pib', ascending=False)
            return df_sorted.to_dict('records')
        
        return pib_data
    
    def analisar_correlacao_pib_idh(self, pib_data, idh_data):
        """Analisa correlação REAL entre PIB e IDH"""
        if not pib_data:
            return {'correlacao': 0, 'mensagem': 'Dados insuficientes'}
        
        df = pd.DataFrame(pib_data)
        
        # Verifica se temos as colunas necessárias
        if 'pib' not in df.columns or 'idh' not in df.columns:
            return {'correlacao': 0, 'mensagem': 'Colunas PIB ou IDH não encontradas'}
        
        # Calcula correlação REAL
        correlacao_valor = df['pib'].corr(df['idh'])
        
        # Interpretação da correlação
        if abs(correlacao_valor) > 0.7:
            interpretacao = "Forte correlação positiva"
        elif abs(correlacao_valor) > 0.5:
            interpretacao = "Correlação positiva moderada" 
        elif abs(correlacao_valor) > 0.3:
            interpretacao = "Correlação positiva fraca"
        else:
            interpretacao = "Correlação muito fraca ou inexistente"
        
        return {
            'valor': float(correlacao_valor),  # CONVERTE para float
            'interpretacao': interpretacao,
            'amostra': int(len(df)),  # CONVERTE para int
            'resumo': f"Correlação de {round(correlacao_valor, 3)} entre PIB e IDH"
        }
    
    def comparar_estados(self, estados_data):
        """Compara estados por população"""
        comparacao = []
        
        for estado in estados_data:
            comparacao.append({
                'estado': estado.get('nome', 'N/A'),
                'sigla': estado.get('sigla', 'N/A'),
                'regiao': estado.get('regiao', {}).get('nome', 'N/A'),
                'populacao': int(estado.get('populacao', 0))  # CONVERTE para int
            })
        
        # Ordena por população
        comparacao.sort(key=lambda x: x['populacao'], reverse=True)
        return comparacao
    
    def analisar_distribuicao_regional(self):
        """Analisa distribuição regional dos indicadores"""
        df = pd.DataFrame(dados_estados)
        
        distribuicao = {}
        for regiao in df['regiao'].apply(lambda x: x['nome']).unique():
            dados_regiao = df[df['regiao'].apply(lambda x: x['nome']) == regiao]
            
            # CONVERTE para tipos Python nativos (int/float)
            distribuicao[regiao] = {
                'total_estados': int(len(dados_regiao)),
                'populacao_total': int(dados_regiao['populacao'].sum()),
                'populacao_media': float(dados_regiao['populacao'].mean()),
                'estados': dados_regiao[['sigla', 'nome', 'populacao']].to_dict('records')
            }
        
        return distribuicao
    
    def calcular_estatisticas_descritivas(self, dados):
        """Calcula estatísticas descritivas"""
        if not dados:
            return {}
        
        df = pd.DataFrame(dados)
        estatisticas = {}
        
        for coluna in df.select_dtypes(include=[np.number]).columns:
            valores = df[coluna].dropna()
            
            if len(valores) > 0:
                # CONVERTE todos os valores para tipos Python nativos
                estatisticas[coluna] = {
                    'media': float(valores.mean()),
                    'mediana': float(valores.median()),
                    'desvio_padrao': float(valores.std()),
                    'minimo': float(valores.min()),
                    'maximo': float(valores.max()),
                    'contagem': int(len(valores))
                }
        
        return estatisticas

# Instância da análise
analise = AnaliseDemografica()

@ns_estados.route('/')
class ListaEstados(Resource):
    def get(self):
        """Lista todos os estados brasileiros"""
        return jsonify({
            'status': 'success',
            'total': len(dados_estados),
            'estados': dados_estados,
            'timestamp': datetime.now().isoformat()
        })

@ns_estados.route('/<string:sigla>')
class EstadoPorSigla(Resource):
    def get(self, sigla):
        """Dados de um estado específico"""
        estado = next((e for e in dados_estados if e['sigla'] == sigla.upper()), None)
        
        if estado:
            return jsonify({
                'status': 'success',
                'estado': estado,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Estado não encontrado'
            }), 404

@ns_municipios.route('/pib')
class PIBMunicipios(Resource):
    def get(self):
        """PIB dos municípios"""
        return jsonify({
            'status': 'success',
            'total': len(dados_pib_idh),
            'dados': dados_pib_idh,
            'timestamp': datetime.now().isoformat()
        })

@ns_municipios.route('/idh')
class IDHMunicipios(Resource):
    def get(self):
        """IDH dos municípios"""
        # Usamos os mesmos dados pois já temos PIB e IDH juntos
        return jsonify({
            'status': 'success',
            'total': len(dados_pib_idh),
            'dados': [{'municipio': d['municipio'], 'estado': d['estado'], 'idh': d['idh']} for d in dados_pib_idh],
            'timestamp': datetime.now().isoformat()
        })

@ns_analise.route('/ranking-pib')
class RankingPIB(Resource):
    def get(self):
        """Ranking de municípios por PIB"""
        ranking = analise.criar_ranking_pib(dados_pib_idh)
        
        return jsonify({
            'status': 'success',
            'ranking': ranking,
            'timestamp': datetime.now().isoformat()
        })

@ns_analise.route('/correlacao-pib-idh')
class CorrelacaoPIBIDH(Resource):
    def get(self):
        """Correlação REAL entre PIB e IDH"""
        correlacao = analise.analisar_correlacao_pib_idh(dados_pib_idh, dados_pib_idh)
        
        return jsonify({
            'status': 'success',
            'correlacao': correlacao,
            'timestamp': datetime.now().isoformat()
        })

@ns_analise.route('/estados-comparacao')
class ComparacaoEstados(Resource):
    def get(self):
        """Comparação entre estados"""
        comparacao = analise.comparar_estados(dados_estados)
        
        return jsonify({
            'status': 'success',
            'comparacao': comparacao,
            'timestamp': datetime.now().isoformat()
        })

@ns_analise.route('/distribuicao-regional')
class DistribuicaoRegional(Resource):
    def get(self):
        """Distribuição regional dos indicadores"""
        distribuicao = analise.analisar_distribuicao_regional()
        
        return jsonify({
            'status': 'success',
            'distribuicao': distribuicao,
            'timestamp': datetime.now().isoformat()
        })

@ns_analise.route('/estatisticas-pib')
class EstatisticasPIB(Resource):
    def get(self):
        """Estatísticas descritivas do PIB"""
        estatisticas = analise.calcular_estatisticas_descritivas(dados_pib_idh)
        
        return jsonify({
            'status': 'success',
            'estatisticas': estatisticas,
            'timestamp': datetime.now().isoformat()
        })

@ns_analise.route('/populacao-total')
class PopulacaoTotal(Resource):
    def get(self):
        """Análise da população total"""
        df = pd.DataFrame(dados_estados)
        
        # CONVERTE todos os valores para tipos Python nativos
        populacao_por_regiao = {}
        for regiao, populacao in df.groupby(df['regiao'].apply(lambda x: x['nome']))['populacao'].sum().items():
            populacao_por_regiao[regiao] = int(populacao)  # CONVERTE para int
        
        analise_populacao = {
            'populacao_total': int(df['populacao'].sum()),
            'media_estados': int(df['populacao'].mean()),
            'estado_mais_populoso': df.loc[df['populacao'].idxmax()].to_dict(),
            'estado_menos_populoso': df.loc[df['populacao'].idxmin()].to_dict(),
            'populacao_por_regiao': populacao_por_regiao
        }
        
        return jsonify({
            'status': 'success',
            'analise': analise_populacao,
            'timestamp': datetime.now().isoformat()
        })

# Health Check
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'api': 'IBGE Dados Abertos - Versão Simplificada'
    })

@app.route('/')
def home():
    return jsonify({
        'message': 'API Análise Dados IBGE - Bem vindo!',
        'endpoints': {
            'documentacao': '/docs',
            'health': '/health',
            'estados': '/estados/*',
            'municipios': '/municipios/*', 
            'analise': '/analise/*'
        },
        'exemplos': {
            'listar_estados': '/estados/',
            'estado_sp': '/estados/SP',
            'pib_municipios': '/municipios/pib',
            'correlacao_pib_idh': '/analise/correlacao-pib-idh',
            'ranking_pib': '/analise/ranking-pib',
            'populacao_total': '/analise/populacao-total',
            'distribuicao_regional': '/analise/distribuicao-regional'
        }
    })

if __name__ == '__main__':
    print("🚀 Inicializando API IBGE...")
    print("📊 Endpoints disponíveis:")
    print("   - http://localhost:5000/docs (Documentação)")
    print("   - http://localhost:5000/estados/ (Lista estados)")
    print("   - http://localhost:5000/analise/correlacao-pib-idh (Correlação PIB-IDH)")
    print("   - http://localhost:5000/analise/ranking-pib (Ranking PIB)")
    print("   - http://localhost:5000/analise/populacao-total (Análise população)")
    print("   - http://localhost:5000/analise/distribuicao-regional (Distribuição regional)")
    
    app.run(debug=True, host='0.0.0.0', port=5000)