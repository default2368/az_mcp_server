from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import requests

app = FastAPI()

# Simula un Tool
@app.post("/tools/get_weather", response_model=Dict)
async def get_weather(location: str):
    """
    Simula un tool che restituisce il meteo per una posizione specificata.
    """
    return {
        "temperature": 72,
        "conditions": "Sunny",
        "humidity": 45
    }

# Nuovo Tool con dati dinamici da OpenWeatherMap
@app.post("/tools/get_weather_dynamic", response_model=Dict)
async def get_weather_dynamic(location: str):
    """
    Recupera dati meteo reali da OpenWeatherMap.
    """
    API_KEY = "065b58bec3b0400f679e81d85fe35378"  # Assicurati di usare una chiave valida
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
    
    # Fai la richiesta HTTP
    response = requests.get(url)
    
    # Debug: Stampa la risposta completa
    print("OpenWeatherMap Response:", response.text)
    
    # Controlla lo stato della risposta
    if response.status_code == 200:
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "conditions": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"]
        }
    else:
        raise HTTPException(status_code=400, detail=f"Error fetching weather data: {response.status_code}")

# Simula un Resource
@app.get("/resources/read_file", response_model=Dict)
async def read_file(file_path: str):
    """
    Simula un resource che legge il contenuto di un file.
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return {"content": content}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")

# Simula un Prompt
class CodeReviewRequest(BaseModel):
    code: str
    language: str

@app.post("/prompts/code_review", response_model=List[Dict])
async def code_review(request: CodeReviewRequest):
    """
    Simula un prompt per generare una revisione del codice.
    """
    return [
        {"role": "system", "content": f"You are reviewing {request.language} code."},
        {"role": "user", "content": f"Please review:\n\n{request.code}"}
    ]

# Simula un Sampling Request
class SamplingRequest(BaseModel):
    messages: List[Dict]

@app.post("/sampling/request_sampling", response_model=Dict)
async def request_sampling(request: SamplingRequest):
    """
    Simula una richiesta di sampling.
    """
    return {
        "role": "assistant",
        "content": "Analysis of the provided data..."
    }

# Simula il Discovery Process
@app.get("/capabilities/discovery", response_model=Dict)
async def discovery():
    """
    Simula il processo di discovery delle capacità MCP.
    """
    return {
        "tools": ["get_weather"],
        "resources": ["read_file"],
        "prompts": ["code_review"],
        "sampling": ["request_sampling"]
    }			
