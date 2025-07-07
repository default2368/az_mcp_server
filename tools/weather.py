"""
Modulo per i tool meteo MCP
"""

import requests
from fastapi import HTTPException
from typing import Dict

async def get_weather(location: str) -> Dict:
    """
    Simula un tool che restituisce il meteo per una posizione specificata.
    """
    return {
        "temperature": 72,
        "conditions": "Sunny",
        "humidity": 45,
        "location": location
    }

async def get_weather_dynamic(location: str) -> Dict:
    """
    Recupera dati meteo reali da OpenWeatherMap.
    """
    API_KEY = "065b58bec3b0400f679e81d85fe35378"  # Sarebbe meglio usare una variabile d'ambiente
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "conditions": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "location": location
        }
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=400,
            detail=f"Errore durante il recupero dei dati meteo: {str(e)}"
        )
