"""Expert selector module"""
import logging
from typing import Tuple, Optional
from src.utils.openai_client import OpenAIClient

class ExpertSelector:
    """Expert selector class for routing queries to appropriate experts"""
    
    def __init__(self):
        """Initialize expert selector"""
        self.logger = logging.getLogger(__name__)
        self.openai_client = OpenAIClient(
            model='gpt-4',
            max_tokens=100,
            temperature=0.3
        )
        
    async def select_expert(self, query: str) -> Tuple[Optional[str], Optional[str]]:
        """Select appropriate expert for query
        
        Args:
            query (str): User query
            
        Returns:
            Tuple[Optional[str], Optional[str]]: Expert type and direct response if no expert needed
        """
        try:
            system_prompt = """You are an expert classifier. Your task is to determine which expert should handle a given query.
            Available experts are:
            - sports: For sports and fitness related queries
            - food: For food, cooking, and nutrition related queries
            - ai: For artificial intelligence and technology related queries
            - sudostar: For questions about the SudoStar mobile application
            - general: For general queries like weather, news, facts etc.
            
            Respond with ONLY the expert type (sports/food/ai/sudostar/general)."""
            
            response = await self.openai_client.get_completion(system_prompt, query)
            if not response:
                return None, None
                
            # Parse response
            response = response.strip().lower()
            if response in ['sports', 'food', 'ai', 'sudostar', 'general']:
                return response, None
                
            return 'general', None  # Default to general expert
            
        except Exception as e:
            self.logger.error(f"Error selecting expert: {str(e)}")
            return None, None 