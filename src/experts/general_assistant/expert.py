"""General assistant for handling queries that don't match other experts"""
import logging
import json
from typing import Optional, Dict, Any, List, Tuple
from ..base_expert import BaseExpert
from .sources import (
    get_system_prompt,
    get_user_prompt_template
)

class GeneralAssistant(BaseExpert):
    """Assistant for handling any type of query that doesn't match specialized experts"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize general assistant"""
        super().__init__(config)
        self.logger = logging.getLogger(__name__)
        
    async def get_response(self, query: str) -> Optional[Dict[str, Any]]:
        """Generate response for any type of query using multiple sources
        
        Args:
            query (str): User query
            
        Returns:
            Optional[Dict[str, Any]]: Response dictionary or None if failed
        """
        try:
            # 1. Local data kontrolü
            local_response = await self._check_local_data(query)
            if local_response:
                verified_response = await self._verify_with_openai(local_response, query, "local")
                if verified_response:
                    return verified_response

            # 2. URL kaynaklarını kontrol et
            url_response = await self._check_url_sources(query)
            if url_response:
                verified_response = await self._verify_with_openai(url_response, query, "url")
                if verified_response:
                    return verified_response

            # 3. Web araması yap
            web_results = await self._perform_web_search(query)
            if web_results:
                web_response = await self._generate_response(web_results, query)
                if web_response:
                    return web_response

            # 4. Hiçbir kaynak bulunamazsa OpenAI'ya sor
            return await self._fallback_to_openai(query)
            
        except Exception as e:
            self.logger.error(f"Error generating response: {str(e)}")
            return None

    async def _check_local_data(self, query: str) -> Optional[Dict[str, Any]]:
        """Check local knowledge base for answer"""
        try:
            # TODO: Implement local data check
            # Örnek: Tarih, saat, basit hesaplamalar vs.
            return None
        except Exception as e:
            self.logger.error(f"Error checking local data: {str(e)}")
            return None

    async def _check_url_sources(self, query: str) -> Optional[Dict[str, Any]]:
        """Check predefined URL sources for answer"""
        try:
            # TODO: Implement URL source check
            # Örnek: Hava durumu, döviz, haberler vs.
            return None
        except Exception as e:
            self.logger.error(f"Error checking URL sources: {str(e)}")
            return None

    async def _verify_with_openai(self, response: Dict[str, Any], query: str, source: str) -> Optional[Dict[str, Any]]:
        """Verify and enhance response using OpenAI"""
        try:
            system_prompt = f"""Verilen yanıtı kontrol et ve geliştir.
            Kaynak: {source}
            
            Kontrol kriterleri:
            1. Yanıt soruyla alakalı mı?
            2. Bilgiler doğru ve güncel mi?
            3. Yanıt yeterince açıklayıcı mı?
            
            Eğer yanıt uygunsa geliştir, değilse None döndür."""

            user_prompt = f"""Soru: {query}
            Yanıt: {response.get('text', '')}"""

            verification = await self.openai_client.get_completion(system_prompt, user_prompt)
            if verification.lower().strip() == "none":
                return None

            response["text"] = verification
            response["verified"] = True
            return response

        except Exception as e:
            self.logger.error(f"Error verifying with OpenAI: {str(e)}")
            return None

    async def _generate_response(self, documents: List[str], message: str) -> Optional[Dict[str, Any]]:
        """Generate response using web search results and AI"""
        if not documents:
            return None
            
        system_prompt = get_system_prompt()
        user_prompt = get_user_prompt_template().format(
            query=message,
            search_results="\n".join(documents)
        )
        
        try:
            response = await self.openai_client.get_completion(system_prompt, user_prompt)
            result = json.loads(response)
            
            # Güven skoru kontrolü
            if result.get("confidence", 0) < 0.7:
                result["is_supported"] = False
            else:
                result["is_supported"] = True
                result["source"] = "web_search"
                
            return result
        except Exception as e:
            self.logger.error(f"Error generating response: {str(e)}")
            return None

    async def _fallback_to_openai(self, query: str) -> Optional[Dict[str, Any]]:
        """Generate response using only OpenAI when no other sources available"""
        try:
            system_prompt = """Sen genel bilgi asistanısın. Soruya mevcut bilgilerinle
            en iyi şekilde cevap ver. Emin olmadığın konularda bunu belirt."""

            user_prompt = f"Soru: {query}"

            response = await self.openai_client.get_completion(system_prompt, user_prompt)
            return {
                "text": response,
                "is_supported": False,
                "confidence": 0.5,
                "source": "openai_only"
            }

        except Exception as e:
            self.logger.error(f"Error in OpenAI fallback: {str(e)}")
            return None 