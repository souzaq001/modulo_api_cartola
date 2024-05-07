import requests
import pandas as pd

class CartolaAPI:
    """
    Classe para interagir com a API do Cartola.
    """

    def __init__(self):
        """
        Inicializa a classe CartolaAPI.
        """
        self.base_url = 'https://api.cartola.globo.com/'

    def request_data(self, url: str) -> dict:
        """
        Faz uma requisição GET à API e retorna os dados JSON.

        Parâmetros:
        url (str): A URL completa para a requisição.

        Retorna:
        dict: Os dados JSON obtidos da API, ou None em caso de erro na requisição.
        """
        try:
            resposta = requests.get(url)
            resposta.raise_for_status()
            return resposta.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição da API: {e}")
            return None

    def get_pontuacoes(self, rodada: str) -> pd.DataFrame:
        """
        Obtém as pontuações dos atletas para uma determinada rodada.

        Parâmetros:
        rodada (str): A rodada para a qual deseja-se obter as pontuações.

        Retorna:
        pandas.DataFrame: Um DataFrame contendo as pontuações dos atletas, ou None em caso de erro.
        """
        url = f"{self.base_url}atletas/pontuados/{rodada}"
        objetos = self.request_data(url)
        if objetos:
            try:
                df = pd.json_normalize(objetos['atletas'].values())
                return df
            except (KeyError, TypeError) as e:
                print(f"Erro ao normalizar os dados JSON: {e}")
                return None

    def get_mercado(self, mercado_info: str) -> pd.DataFrame:
        """
        Obtém informações sobre o mercado do Cartola.

        Parâmetros:
        mercado_info (str): Informação específica do mercado desejada, como 'clubes', 'posicoes', 'status' ou 'atletas'.

        Retorna:
        pandas.DataFrame: Um DataFrame contendo as informações do mercado, ou None em caso de erro.
        """
        url = f"{self.base_url}atletas/mercado/"
        objetos = self.request_data(url)
        if objetos:
            try:
                if mercado_info == 'atletas':
                    df = pd.json_normalize(objetos[mercado_info])
                    return df
                else:
                    df = pd.json_normalize(objetos[mercado_info].values())
                    return df
            except (KeyError, TypeError) as e:
                print(f"Erro ao normalizar os dados JSON: {e}")
                return None

    def get_partidas(self) -> pd.DataFrame:
        """
        Obtém informações sobre as partidas do Cartola.

        Retorna:
        pandas.DataFrame: Um DataFrame contendo as informações sobre as partidas, ou None em caso de erro.
        """
        url = f"{self.base_url}partidas/"
        objetos = self.request_data(url)
        if objetos:
            try:
                df = pd.json_normalize(objetos['partidas'])
                return df
            except (KeyError, TypeError) as e:
                print(f"Erro ao normalizar os dados JSON: {e}")
                return None
