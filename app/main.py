from fastapi import FastAPI, Query
import http.client
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

AGENT_API_FUTEBOL = os.getenv("AGENT_API_FUTEBOL")
HEADERS = {
  "X-RapidAPI-Key": AGENT_API_FUTEBOL, 
  "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

def get_team_id(team_name: str):
  url = "https://api-football-v1.p.rapidapi.com"
  params = {"search": team_name}
  response = requests.get(url, headers=HEADERS, params=params)
  data = response.json()

  if data["response"]:
    return data ["response"][0]["team"]["id"]
  else:
    return None

@app.get("/proximo-jogo")
def proximo_jogo(time: str = Query(..., description="Nome do time, ex: Flamengo")):   
  try:
    team_id = get_team_id(time)
    if not team_id:
      return {"error": "Time não encontrado"}
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    params = {"team": team_id, "next": 1}
    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()  

    if not data["response"]:
        return {"message": f"Não encontrei próximos jogos para {time}"}

    jogo = data["response"][0]
    adversario = (
      jogo["teams"]["home"]["name"]
      if jogo["teams"]["away"]["name"].lower() == time.lower()
      else jogo["teams"]["away"]["name"]
    )

    return {
      "time": time,
      "adversario": adversario,
      "data": jogo["fixture"]["date"],
      "estadio": jogo["fixture"]["venue"]["name"],
      "transmissao": jogo["fixture"].get("broadcast", "Ainda não divulgado")
    }

  except Exception as e:
    return {"error": f"Erro ao buscar jogo: {str(e)}"}   

@app.get("/countries")
def get_countries():
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': AGENT_API_FUTEBOL
    }
    conn.request("GET", "/countries", headers=headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")     