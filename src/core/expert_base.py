"""Base class for all experts"""
from typing import Optional, Tuple, List
import logging
import aiohttp
from bs4 import BeautifulSoup
from src.utils.openai_client import OpenAIClient
from src.utils.web_search import WebSearch
from src.utils.cache import Cache
import time
import openai
import asyncio

logger = logging.getLogger(__name__)

class ExpertBase:
    def __init__(self, expert_type: str):
        """Initialize expert
        
        Args:
            expert_type (str): Type of expert (sports, food, ai, sudostar)
        """
        self.expert_type = expert_type
        self.openai_client = OpenAIClient()
        self.web_search = WebSearch()
        self.cache = Cache()
        
    async def get_response(self, question: str) -> Optional[str]:
        """Get response using multiple data sources:
        1. Local data (knowledge base)
        2. OpenAI API
        3. URL content
        4. Web search
        
        Args:
            question (str): User's question
            
        Returns:
            Optional[str]: Response or None if no answer found
        """
        try:
            # 1. Try OpenAI first for most up-to-date response
            if ai_answer := await self._get_ai_answer(question):
                logger.info("Generated answer with OpenAI")
                self.cache.set(question, {
                    'response': ai_answer,
                    'timestamp': time.time()
                })
                return ai_answer
                
            # 2. Check cache if AI fails
            if cached := self.cache.get(question):
                if time.time() - cached.get('timestamp', 0) < 3600:
                    logger.info("Cache hit")
                    return cached.get('response')
                else:
                    logger.info("Cache expired")
                    self.cache.delete(question)
                
            # 3. Try local knowledge base
            if local_answer := await self._get_local_answer(question):
                logger.info("Found answer in local data")
                self.cache.set(question, {
                    'response': local_answer,
                    'timestamp': time.time()
                })
                return local_answer
                
            # 4. Try URL content
            if url_answer := await self._get_url_content(question):
                logger.info("Found answer in URL content")
                self.cache.set(question, {
                    'response': url_answer,
                    'timestamp': time.time()
                })
                return url_answer
                
            # 5. Try web search as last resort
            if web_answer := await self._get_web_answer(question):
                logger.info("Found answer from web search")
                self.cache.set(question, {
                    'response': web_answer,
                    'timestamp': time.time()
                })
                return web_answer
                
            logger.warning("No answer found from any source")
            return "Üzgünüm, bu soruya yanıt bulamadım. Lütfen soruyu farklı bir şekilde sormayı deneyin."
            
        except Exception as e:
            logger.error(f"Error getting response: {str(e)}", exc_info=True)
            return "Bir hata oluştu. Lütfen daha sonra tekrar deneyin."
            
    async def _get_local_answer(self, question: str) -> Optional[str]:
        """Get answer from local knowledge base
        
        Args:
            question (str): User's question
            
        Returns:
            Optional[str]: Answer if found in local data
        """
        try:
            if hasattr(self, 'find_answer'):
                return await self.find_answer(question)
            return None
        except Exception as e:
            logger.error(f"Error getting local answer: {str(e)}")
            return None
            
    async def _get_ai_answer(self, question: str) -> Optional[str]:
        """Get answer from OpenAI
        
        Args:
            question (str): User's question
            
        Returns:
            Optional[str]: Generated answer from OpenAI
        """
        try:
            system_prompt = f"""Sen bir {self.expert_type} uzmanısın.
            Kullanıcının sorduğu soruları detaylı ve doğru şekilde yanıtla.
            Eğer soruyu yanıtlayamıyorsan veya emin değilsen, bunu belirt."""
            
            max_retries = 3
            retry_count = 0
            
            while retry_count < max_retries:
                try:
                    return await self.openai_client.get_completion(system_prompt, question)
                except openai.error.RateLimitError:
                    logger.warning("Rate limit hit, waiting before retry...")
                    await asyncio.sleep(2 ** retry_count)  # Exponential backoff
                    retry_count += 1
                except openai.error.APIError as e:
                    if "internal_server_error" in str(e):
                        logger.warning("OpenAI server error, retrying...")
                        await asyncio.sleep(1)
                        retry_count += 1
                    else:
                        raise
            
            logger.error("Max retries reached for OpenAI API")
            return "Üzgünüm, şu anda yanıt üretmekte sorun yaşıyorum. Lütfen daha sonra tekrar deneyin."
            
        except Exception as e:
            logger.error(f"Error getting AI answer: {str(e)}", exc_info=True)
            if "insufficient_quota" in str(e):
                return "API kotası doldu. Lütfen sistem yöneticisiyle iletişime geçin."
            elif "invalid_api_key" in str(e):
                return "API yapılandırma hatası. Lütfen sistem yöneticisiyle iletişime geçin."
            return None
            
    async def _get_url_content(self, question: str) -> Optional[str]:
        """Get answer from relevant URLs
        
        Args:
            question (str): User's question
            
        Returns:
            Optional[str]: Answer extracted from URLs
        """
        try:
            # Get relevant URLs for the expert type
            urls = self._get_expert_urls()
            
            if not urls:
                return None
                
            # Fetch and parse content from URLs
            async with aiohttp.ClientSession() as session:
                for url in urls:
                    try:
                        async with session.get(url) as response:
                            if response.status == 200:
                                html = await response.text()
                                soup = BeautifulSoup(html, 'html.parser')
                                
                                # Remove script and style elements
                                for script in soup(["script", "style"]):
                                    script.decompose()
                                    
                                # Get text content
                                text = soup.get_text()
                                
                                # Use OpenAI to extract relevant answer
                                system_prompt = """Verilen metin içeriğinden soruya en uygun yanıtı çıkar.
                                Eğer uygun yanıt bulunamazsa None döndür."""
                                
                                user_prompt = f"""Soru: {question}
                                
                                Metin: {text[:2000]}  # İlk 2000 karakter
                                
                                Yanıt:"""
                                
                                if answer := await self.openai_client.get_completion(system_prompt, user_prompt):
                                    if answer.lower() != "none":
                                        return answer
                                        
                    except Exception as e:
                        logger.error(f"Error fetching URL {url}: {str(e)}")
                        continue
                        
            return None
            
        except Exception as e:
            logger.error(f"Error getting URL content: {str(e)}")
            return None
            
    async def _get_web_answer(self, question: str) -> Optional[str]:
        """Get answer from web search
        
        Args:
            question (str): User's question
            
        Returns:
            Optional[str]: Answer from web search
        """
        try:
            return await self.web_search.search(question)
        except Exception as e:
            logger.error(f"Error getting web answer: {str(e)}")
            return None
            
    def _get_expert_urls(self) -> List[str]:
        """Get relevant URLs for the expert type
        
        Returns:
            List[str]: List of relevant URLs
        """
        # Her expert kendi URL'lerini override edebilir
        return [] 