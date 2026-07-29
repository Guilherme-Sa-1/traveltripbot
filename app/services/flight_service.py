import os
import requests
from datetime import datetime

class FlightService:
    def __init__(self):
        self.api_key = os.getenv("SERPAPI_KEY")
        self.base_url = "https://serpapi.com/search.json"

    def format_date(self, date_str: str) -> str:
        
        date_obj = datetime.strptime(date_str, "%d/%m/%Y")
        return date_obj.strftime("%Y-%m-%d")

    def search_flights(
        self, 
        origin: str, 
        destination: str, 
        departure_date: str, 
        return_date: str, 
        adults: int
    ) -> dict:
        
        params = {
            "engine": "google_flights",
            "departure_id": origin,      
            "arrival_id": destination,   
            "outbound_date": self.format_date(departure_date),
            "return_date": self.format_date(return_date),
            "adults": adults,
            "currency": "BRL",            
            "hl": "pt",                  
            "api_key": self.api_key
        }
        
        response = requests.get(self.base_url, params=params)
        
        return response.json()