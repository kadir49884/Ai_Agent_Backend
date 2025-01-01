"""General expert for basic queries"""
import logging
import json
from datetime import datetime
from typing import Optional, Dict, Any, List
from ..base_expert import BaseExpert

class GeneralExpert(BaseExpert):
    """Expert for handling general queries like date, time, weather, etc."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize general expert"""
        super().__init__(config)
        self.logger = logging.getLogger(__name__)
        
    async def get_response(self, query: str) -> Optional[Dict[str, Any]]:
        """Generate response for general queries
        
        Args:
            query (str): User query
            
        Returns:
            Optional[Dict[str, Any]]: Response dictionary or None if failed
        """
        query = query.lower().strip()
        
        # 1. Önce local knowledge'ı kontrol et
        local_response = await self._check_local_knowledge(query)
        if local_response:
            return local_response
            
        # 2. URL kaynaklarını kontrol et
        url_response = await self._check_url_sources(query)
        if url_response:
            return url_response
            
        # 3. Web araması yap
        web_results = await self._perform_web_search(query)
        
        # 4. AI yanıtı oluştur
        return await self._generate_response(web_results, query)
        
    async def _check_local_knowledge(self, query: str) -> Optional[Dict[str, Any]]:
        """Check local knowledge for basic queries like date, time etc."""
        # Tarih sorgusu
        if any(keyword in query for keyword in ["bugün", "tarih", "günlerden", "ayın kaçı"]):
            try:
                now = datetime.now()
                date_str = now.strftime("%d %B %Y %A")
                return {
                    "text": f"Bugün {date_str}",
                    "is_supported": True,
                    "confidence": 1.0
                }
            except Exception as e:
                self.logger.error(f"Error getting date: {str(e)}")
                
        return None
        
    async def _check_url_sources(self, query: str) -> Optional[Dict[str, Any]]:
        """Check predefined URLs for current information"""
        try:
            # Hava durumu için AccuWeather
            if "hava" in query:
                weather_data = await self._fetch_weather_data()
                if weather_data:
                    return {
                        "text": weather_data,
                        "is_supported": True,
                        "confidence": 0.9
                    }
                    
            # Döviz kurları için TCMB
            if any(keyword in query for keyword in ["döviz", "kur", "euro", "dolar"]):
                exchange_data = await self._fetch_exchange_rates()
                if exchange_data:
                    return {
                        "text": exchange_data,
                        "is_supported": True,
                        "confidence": 0.9
                    }
                    
        except Exception as e:
            self.logger.error(f"Error checking URL sources: {str(e)}")
            
        return None
        
    async def _generate_response(self, documents: List[str], message: str) -> Optional[Dict[str, Any]]:
        """Generate response using web search results and AI"""
        if not documents:
            return None
            
        system_prompt = """Sen genel konularda uzman bir asistansın.
        Verilen web arama sonuçlarını kullanarak soruya kapsamlı ve doğru bir yanıt üretmelisin.
        Yanıt üretirken şu kurallara uy:
        1. Web arama sonuçlarındaki bilgilerin doğruluğunu kontrol et
        2. Bilgilerin güncelliğini kontrol et
        3. Çelişkili bilgiler varsa en güvenilir kaynağı seç
        4. Emin olmadığın bilgileri verme
        5. Yanıtı kullanıcı dostu ve anlaşılır bir dille ver
        6. Sayısal veriler varsa bunları düzgün formatla
        7. Güncel olması gereken bilgiler için tarihi mutlaka belirt"""
        
        user_message = f"""Soru: {message}
        
        Web arama sonuçları:
        {chr(10).join(documents)}
        
        Bu bilgileri kullanarak soruya yanıt ver."""
        
        try:
            response = await self.openai_client.get_completion(system_prompt, user_message)
            result = json.loads(response)
            
            # Güven skoru yeterince yüksek değilse desteklenmez olarak işaretle
            if result.get("confidence", 0) < 0.7:
                result["is_supported"] = False
                
            return result
        except Exception as e:
            self.logger.error(f"Error generating response: {str(e)}")
            return None
            
    async def _fetch_weather_data(self) -> Optional[str]:
        """Fetch current weather data"""
        # TODO: AccuWeather API entegrasyonu
        return None
        
    async def _fetch_exchange_rates(self) -> Optional[str]:
        """Fetch current exchange rates"""
        # TODO: TCMB API entegrasyonu
        return None 