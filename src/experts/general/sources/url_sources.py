"""General Expert için URL kaynakları"""
from typing import Dict, Any, Optional
import os
import aiohttp
from datetime import datetime

class WeatherAPI:
    """AccuWeather API istemcisi"""
    
    def __init__(self):
        self.api_key = os.getenv('ACCUWEATHER_API_KEY')
        self.base_url = "http://dataservice.accuweather.com"
        
    async def get_current_conditions(self, location_key: str) -> Optional[Dict[str, Any]]:
        """Güncel hava durumunu getir"""
        if not self.api_key:
            return None
            
        url = f"{self.base_url}/currentconditions/v1/{location_key}"
        params = {
            "apikey": self.api_key,
            "language": "tr-tr",
            "details": True
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data[0] if data else None
        except Exception:
            return None

class ExchangeAPI:
    """TCMB Döviz API istemcisi"""
    
    def __init__(self):
        self.base_url = "https://www.tcmb.gov.tr/kurlar"
        
    async def get_exchange_rates(self) -> Optional[Dict[str, Any]]:
        """Güncel döviz kurlarını getir"""
        today = datetime.now().strftime("%Y%m")
        url = f"{self.base_url}/{today}/today.xml"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        # XML'i parse et
                        text = await response.text()
                        # TODO: XML parsing
                        return {}
        except Exception:
            return None

class NewsAPI:
    """Haber API istemcisi"""
    
    def __init__(self):
        self.api_key = os.getenv('NEWS_API_KEY')
        self.base_url = "https://newsapi.org/v2"
        
    async def get_top_headlines(self, category: str = None, query: str = None) -> Optional[Dict[str, Any]]:
        """Son dakika haberlerini getir"""
        if not self.api_key:
            return None
            
        url = f"{self.base_url}/top-headlines"
        params = {
            "apiKey": self.api_key,
            "country": "tr",
            "language": "tr"
        }
        
        if category:
            params["category"] = category
        if query:
            params["q"] = query
            
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        return await response.json()
        except Exception:
            return None

# API istemcilerini oluştur
weather_api = WeatherAPI()
exchange_api = ExchangeAPI()
news_api = NewsAPI() 