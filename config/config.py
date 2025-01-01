"""Configuration module"""
import os
from typing import Dict, Any

def load_config() -> Dict[str, Any]:
    """Load configuration"""
    return {
        'app': APP_CONFIG,
        'experts': EXPERT_CONFIG
    }

APP_CONFIG = {
    'debug': True,
    'host': '0.0.0.0',
    'port': int(os.getenv('PORT', 5000))
}

EXPERT_CONFIG = {
    'sports': {
        'name': 'SportsExpert',
        'openai': {
            'model': 'gpt-4',
            'max_tokens': 300,
            'temperature': 0.7
        },
        'tavily': {
            'max_results': 5,
            'search_depth': 'advanced'
        }
    },
    'food': {
        'name': 'FoodExpert',
        'openai': {
            'model': 'gpt-4',
            'max_tokens': 300,
            'temperature': 0.7
        },
        'tavily': {
            'max_results': 5,
            'search_depth': 'advanced'
        }
    },
    'ai': {
        'name': 'AIExpert',
        'openai': {
            'model': 'gpt-4',
            'max_tokens': 300,
            'temperature': 0.7
        },
        'tavily': {
            'max_results': 5,
            'search_depth': 'advanced'
        }
    },
    'general': {
        'name': 'GeneralExpert',
        'openai': {
            'model': 'gpt-4',
            'max_tokens': 300,
            'temperature': 0.7
        },
        'tavily': {
            'max_results': 5,
            'search_depth': 'advanced'
        },
        'weather_api': {
            'api_key': os.getenv('WEATHER_API_KEY'),
            'base_url': 'http://api.weatherapi.com/v1'
        },
        'exchange_api': {
            'api_key': os.getenv('EXCHANGE_API_KEY'),
            'base_url': 'https://api.exchangerate-api.com/v4/latest'
        }
    }
} 