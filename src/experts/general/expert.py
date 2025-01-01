"""General expert module for handling general queries"""
import logging
from typing import Optional
from src.core.base_expert import BaseExpert
from src.utils.web_search import WebSearch
from src.utils.event_bus import EventBus

class GeneralExpert(BaseExpert):
    """Expert for handling general queries using web search"""
    
    def __init__(self, config: dict):
        """Initialize general expert
        
        Args:
            config (dict): Expert configuration
        """
        super().__init__(config['name'])
        self.logger = logging.getLogger(__name__)
        self.web_search = WebSearch()
        self.event_bus = EventBus()
        
        # Subscribe to events
        self.event_bus.subscribe('question_received', self._on_question_received)
        self.event_bus.subscribe('response_generated', self._on_response_generated)
        
    async def get_response(self, query: str) -> Optional[str]:
        """Get response for general query
        
        Args:
            query (str): User query
            
        Returns:
            Optional[str]: Response or None if failed
        """
        try:
            # Check cache first
            if self.cache:
                cached_response = self.cache.get(query)
                if cached_response:
                    self.logger.info("Cache hit")
                    return cached_response
            
            # Generate response using OpenAI
            system_prompt = """Sen genel konularda uzman bir asistansın. 
            Hava durumu, haberler, tarih, coğrafya ve genel kültür konularında bilgi sahibisin.
            Soruları kısa ve öz bir şekilde yanıtla. Emin olmadığın konularda bunu belirt.
            Yanıtlarında güncel ve doğru bilgiler vermeye özen göster."""
            
            ai_response = await self.openai_client.get_completion(system_prompt, query)
            if ai_response:
                if self.cache:
                    self.cache.set(query, ai_response)
                self.logger.info("Generated response using OpenAI")
                return ai_response
            
            # Perform web search as last resort
            self.logger.info("Performing web search")
            results = await self.web_search.search(query)
            if results:
                response = results[0]
                if self.cache:
                    self.cache.set(query, response)
                return response
            
            return "Üzgünüm, bu soruya yanıt bulamadım. Lütfen soruyu daha açık bir şekilde sorar mısınız?"
            
        except Exception as e:
            self.logger.error(f"Error generating general response: {str(e)}")
            return None
            
    async def _on_question_received(self, data: dict) -> None:
        """Handle received question event
        
        Args:
            data (dict): Event data containing question
        """
        self.logger.info(f"General expert received question: {data.get('message', '')}")
        
    async def _on_response_generated(self, data: dict) -> None:
        """Handle generated response event
        
        Args:
            data (dict): Event data containing response
        """
        self.logger.info(f"General expert generated response: {data.get('response', '')}")
        
    def _format_response(self, response: str) -> str:
        """Format the response to be more user-friendly
        
        Args:
            response (str): Raw response
            
        Returns:
            str: Formatted response
        """
        try:
            # Remove extra whitespace
            response = ' '.join(response.split())
            
            # Add emoji based on content
            if "hava" in response.lower():
                response = "🌤️ " + response
            elif "saat" in response.lower():
                response = "⌚ " + response
            elif "tarih" in response.lower():
                response = "📅 " + response
                
            return response
            
        except Exception as e:
            self.logger.error(f"Error formatting response: {str(e)}")
            return response 