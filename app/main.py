from fastapi import FastAPI
import os
import requests
from dotenv import load_dotenv

load_dotenv() # Função pronta do pacote python-dotenv que busca um arquivo .env no projeto e carrega suas variáveis para o ambiente do sistema
app = FastAPI()  # Cria uma "instância" = Faz como se estivesse construindo um objeto FastAPI na memória. 

API_KEY = os.getenv("API_KEY_FUTEBOL") # Obtém o valor da variável de ambiente "API_KEY_FUTEBOL" que foi carregada do arquivo .env
HEADERS = {"Authorization": f"Bearer {API_KEY}"} # Cria o cabeçalho de autenticação no formato que a API externa exige
BASE_URL = "https://api.api-futebol.com.br/v1"

#listar os campeonatos
@app.get("/campeonatos")
def listar_campeonatos():
    url = f"{BASE_URL}/campeonatos"  # Monta a URL completa juntando base + endpoint específica
    response = requests.get(url, headers=HEADERS) # Faz a chamada REAL para a API externa
    if response.status_code != 200:
        return {"error": f"Erro na requisição: {response.status_code}"}  # Retorna erro personalizado
    
    campeonatos = response.json() # Converte a resposta JSON em lista/dicionário Python
    
    # Retornando apenas os campos mais importantes
    # Filtra apenas os dados importantes para não trafegar informação desnecessária
    resultado = []
    for campeonato in campeonatos:
        resultado.append({ #.append() é um método para ADICIONAR itens a uma lista
            "id": campeonato["campeonato_id"],
            "nome": campeonato["nome"],
            "nome_popular": campeonato["nome_popular"],
            "status": campeonato["status"],
            "tipo": campeonato["tipo"],
        })
    return resultado    

@app.get("/campeonato/{campeonato_id}")
def get_campeonato(campeonato_id: int):
    url = f"{BASE_URL}/campeonatos/{campeonato_id}"
    response = requests.get(url, headers=HEADERS)
    return response.json()

# Rota para pegar os times da fase atual de um campeonato
# @app.get("/campeonato/{campeonato_id}/times")
# def get_teams(campeonato_id: int):
#     # Pega fase atual
#     campeonato = requests.get(f"{BASE_URL}/campeonatos/{campeonato_id}", headers=HEADERS).json()
#     fase_id = campeonato["fase_atual"]["fase_id"]

#     # Pega times da fase
#     url_fase = f"{BASE_URL}/campeonatos/{campeonato_id}/fases/{fase_id}"
#     data_fase = requests.get(url_fase, headers=HEADERS).json()
#     times = []

#     for grupo in data_fase.get("grupos", []):
#         for time in grupo.get("times", []):
#             times.append({
#                 "id": time["time"]["id"],
#                 "nome": time["time"]["nome"],
#                 "sigla": time["time"]["sigla"],
#                 "escudo": time["time"]["escudo"]
#             })

#     # Se não tiver grupos, alguns campeonatos retornam direto
#     if not times and "times" in data_fase:
#         for time in data_fase["times"]:
#             times.append({
#                 "id": time["time"]["id"],
#                 "nome": time["time"]["nome"],
#                 "sigla": time["time"]["sigla"],
#                 "escudo": time["time"]["escudo"]
#             })

#     return times

