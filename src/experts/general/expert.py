"""General expert module for handling general queries"""
import logging
from typing import Optional
from src.core.base_expert import BaseExpert
from src.utils.web_search import WebSearch

class GeneralExpert(BaseExpert):
    """Expert for handling general queries using web search"""
    
    def __init__(self, config: dict):
        """Initialize general expert
        
        Args:
            config (dict): Expert configuration
        """
        super().__init__(config)
        self.logger = logging.getLogger(__name__)
        self.web_search = WebSearch()
        
    async def get_response(self, query: str) -> Optional[str]:
        """Get response for general query
        
        Args:
            query (str): User query
            
        Returns:
            Optional[str]: Response or None if failed
        """
        try:
            # Perform web search
            results = await self.web_search.search(query)
            if not results:
                return "Üzgünüm, bu soruya yanıt bulamadım."
                
            return results[0]
            
        except Exception as e:
            self.logger.error(f"Error generating general response: {str(e)}")
            return None 