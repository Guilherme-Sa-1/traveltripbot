import os
import requests
from datetime import datetime

class FlightService:
    def search_flights(self, origin, destination, departure_date, return_date, adults):
        api_key = os.environ.get("SERPAPI_KEY")
        
        # Converte a data do formato brasileiro (DD/MM/AAAA) para o formato da API (AAAA-MM-DD)
        try:
            ida_obj = datetime.strptime(departure_date, "%d/%m/%Y")
            volta_obj = datetime.strptime(return_date, "%d/%m/%Y")
            outbound_date = ida_obj.strftime("%Y-%m-%d")
            inbound_date = volta_obj.strftime("%Y-%m-%d")
        except ValueError as e:
            print(f"Erro na formatação da data: {e}")
            return {"success": False, "error": "Erro interno de formatação de data."}

        url = "https://serpapi.com/search.json"
        params = {
            "engine": "google_flights",
            "departure_id": origin,
            "arrival_id": destination,
            "outbound_date": outbound_date,
            "return_date": inbound_date,
            "adults": adults,
            "currency": "BRL",
            "hl": "pt-BR",
            "api_key": api_key
        }

        try:
            resposta = requests.get(url, params=params).json()
            
            if "error" in resposta:
                return {"success": False, "error": resposta["error"]}

            # Junta todas as opções que o Google Flights encontrou
            melhores_voos = resposta.get("best_flights", [])
            outros_voos = resposta.get("other_flights", [])
            todos_os_voos = melhores_voos + outros_voos

            if not todos_os_voos:
                return {"success": False, "error": "O Google Flights não encontrou voos para esta janela de datas."}

            # Ordena a lista inteira baseada no preço (do menor para o maior)
            voo_mais_barato = sorted(todos_os_voos, key=lambda x: x.get("price", float('inf')))[0]

            # Extrai os dados do voo mais barato
            preco = voo_mais_barato.get("price")
            voos_detalhes = voo_mais_barato.get("flights", [{}])[0]
            companhia = voos_detalhes.get("airline", "Desconhecida")
            
            # Pega o link direto para a compra
            link = resposta.get("search_metadata", {}).get("google_flights_url", "Link não disponível")

            return {
                "success": True,
                "price": preco,
                "airline": companhia,
                "link": link,
                "origin_name": voos_detalhes.get("departure_airport", {}).get("name", origin),
                "destination_name": voos_detalhes.get("arrival_airport", {}).get("name", destination),
                "date": departure_date
            }

        except Exception as e:
            print(f"Erro ao buscar voos: {e}")
            return {"success": False, "error": "Falha na comunicação com a API de voos."}