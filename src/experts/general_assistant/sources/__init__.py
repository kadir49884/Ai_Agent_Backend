"""Source modules for GeneralAssistant"""

from .openai_prompts import get_system_prompt, get_user_prompt_template
from .local_data import check_local_data
from .url_sources import check_url_sources
from .search_queries import get_search_query

__all__ = [
    'get_system_prompt',
    'get_user_prompt_template',
    'check_local_data',
    'check_url_sources',
    'get_search_query'
] 