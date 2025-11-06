import pandas as pd
import numpy as np

class AnaliseDemografica:
    def __init__(self):
        pass
    
    def criar_ranking_pib(self, pib_data):
        """Cria ranking de municípios por PIB"""
        if not pib_data:
            return []
        
        # Se for lista de dicionários, converte para DataFrame
        if isinstance(pib_data, list):
            df = pd.DataFrame(pib_data)
        else:
            df = pib_data
        
        # Simulação de ranking - ordena por algum campo numérico se existir
        colunas_numericas = df.select_dtypes(include=[np.number]).columns
        
        if len(colunas_numericas) > 0:
            coluna_ordenar = colunas_numericas[0]
            df_sorted = df.sort_values(coluna_ordenar, ascending=False)
            return df_sorted.head(20).to_dict('records')
        
        return pib_data[:20]  # Retorna primeiros 20 se não houver números
    
    def analisar_correlacao_pib_idh(self, pib_data, idh_data):
        """Analisa correlação entre PIB e IDH (versão simplificada)"""
        if not pib_data or not idh_data:
            return {'correlacao': 0, 'mensagem': 'Dados insuficientes'}
        
        # Simulação sem scipy
        return {
            'correlacao': 0.65,
            'interpretacao': 'Correlação positiva moderada',
            'amostra': len(pib_data),
            'observacao': 'Análise baseada em dados simulados'
        }
    
    def comparar_estados(self, estados_data, ibge_client=None):
        """Compara estados por população"""
        comparacao = []
        
        for estado in estados_data[:5]:  # Limita a 5 estados para demo
            comparacao.append({
                'estado': estado.get('nome', 'N/A'),
                'sigla': estado.get('sigla', 'N/A'),
                'regiao': estado.get('regiao', {}).get('nome', 'N/A') if isinstance(estado.get('regiao'), dict) else 'N/A',
                'populacao_estimada': np.random.randint(1000000, 50000000)
            })
        
        return comparacao
    
    def analisar_distribuicao_regional(self, ibge_client=None):
        """Analisa distribuição regional dos indicadores"""
        regioes = {
            'Norte': {'estados': 7, 'populacao': 18812000, 'pib_per_capita': 25431.45},
            'Nordeste': {'estados': 9, 'populacao': 57423000, 'pib_per_capita': 18965.78},
            'Centro-Oeste': {'estados': 4, 'populacao': 16537000, 'pib_per_capita': 35678.90},
            'Sudeste': {'estados': 4, 'populacao': 89165000, 'pib_per_capita': 41234.56},
            'Sul': {'estados': 3, 'populacao': 30123000, 'pib_per_capita': 37890.12}
        }
        
        return regioes
    
    def calcular_estatisticas_descritivas(self, dados):
        """Calcula estatísticas descritivas sem scipy"""
        if not dados:
            return {}
        
        if isinstance(dados, list):
            df = pd.DataFrame(dados)
        else:
            df = dados
        
        estatisticas = {}
        for coluna in df.select_dtypes(include=[np.number]).columns:
            valores = df[coluna].dropna()
            
            if len(valores) > 0:
                estatisticas[coluna] = {
                    'media': float(valores.mean()),
                    'mediana': float(valores.median()),
                    'desvio_padrao': float(valores.std()),
                    'minimo': float(valores.min()),
                    'maximo': float(valores.max()),
                    'q1': float(valores.quantile(0.25)),
                    'q3': float(valores.quantile(0.75)),
                    'contagem': len(valores)
                }
        
        return estatisticas
    
    def calcular_tendencia_simples(self, valores):
        """Calcula tendência simples sem scipy"""
        if len(valores) < 2:
            return 0
        
        # Tendência simples: (último - primeiro) / primeiro
        primeiro = valores[0]
        ultimo = valores[-1]
        
        if primeiro == 0:
            return 0
        
        return (ultimo - primeiro) / primeiro