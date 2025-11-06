import requests
import pandas as pd
import cachetools
import time
from typing import List, Dict, Any

class IBGEClient:
    def __init__(self):
        self.base_url = "https://servicodados.ibge.gov.br/api/v1"
        self.cache = cachetools.TTLCache(maxsize=100, ttl=3600)  # Cache de 1 hora
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Faz requisição para API IBGE com cache"""
        cache_key = f"{endpoint}_{str(params)}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            self.cache[cache_key] = data
            time.sleep(0.1)  # Rate limiting
            return data
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            return {}
    
    def get_estados(self) -> List[Dict]:
        """Obtém lista de estados"""
        return self._make_request("localidades/estados")
    
    def get_municipios_estado(self, estado_id: str) -> List[Dict]:
        """Obtém municípios de um estado"""
        return self._make_request(f"localidades/estados/{estado_id}/municipios")
    
    def get_populacao_estado(self, estado_id: str) -> Dict:
        """Obtém população por estado"""
        return self._make_request(f"projecoes/populacao/{estado_id}")
    
    def get_pib_municipios(self, ano: int = 2020) -> List[Dict]:
        """Obtém PIB dos municípios"""
        params = {"ano": ano}
        return self._make_request("contasnacionais/municipios/pib", params)
    
    def get_taxa_desemprego(self, periodo: str = "202301") -> List[Dict]:
        """Obtém taxa de desemprego"""
        return self._make_request(f"trabalho/rendimento/{periodo}")
    
    def get_idh_municipios(self) -> List[Dict]:
        """Obtém IDH dos municípios"""
        return self._make_request("indicadores-sociais/municipios/idh")
    
    def get_educacao_municipios(self) -> List[Dict]:
        """Obtém dados de educação"""
        return self._make_request("educacao/municipios/matriculas")
    
    def get_saude_municipios(self) -> List[Dict]:
        """Obtém dados de saúde"""
        return self._make_request("saude/municipios/estabelecimentos")
    
    def get_indicadores_estado(self, estado_id: str) -> Dict:
        """Obtém múltiplos indicadores de um estado"""
        populacao = self.get_populacao_estado(estado_id)
        
        return {
            'populacao': populacao,
            'estado_id': estado_id
        }