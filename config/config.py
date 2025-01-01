"""Application configuration"""
import os
from typing import Dict, Any

# Expert system configuration
EXPERT_CONFIG: Dict[str, Dict[str, Any]] = {
    'sports': {
        'name': 'SportsExpert',
        'description': 'Spor ve fitness konularında uzman AI asistan',
        'openai': {
            'model': 'gpt-4',
            'max_tokens': 300,
            'temperature': 0.7
        }
    },
    'food': {
        'name': 'FoodExpert',
        'description': 'Yemek ve beslenme konularında uzman AI asistan',
        'openai': {
            'model': 'gpt-4',
            'max_tokens': 300,
            'temperature': 0.7
        }
    },
    'ai': {
        'name': 'AIExpert',
        'description': 'Yapay zeka ve teknoloji konularında uzman AI asistan',
        'openai': {
            'model': 'gpt-4',
            'max_tokens': 300,
            'temperature': 0.7
        }
    },
    'sudostar': {
        'name': 'SudoStarExpert',
        'description': 'SudoStar uygulaması hakkında uzman AI asistan',
        'openai': {
            'model': 'gpt-4',
            'max_tokens': 300,
            'temperature': 0.7
        }
    },
    'general': {
        'name': 'GeneralAssistant',
        'description': 'Uzman bulunamayan konularda yardımcı olan genel amaçlı AI asistan',
        'openai': {
            'model': 'gpt-4',
            'max_tokens': 500,  # Daha uzun yanıtlar için
            'temperature': 0.8  # Daha yaratıcı yanıtlar için
        },
        'tavily': {
            'api_key': os.getenv('TAVILY_API_KEY'),
            'max_results': 5,
            'search_depth': 'advanced'
        },
        'cache': {
            'enabled': True,
            'ttl': 1800  # 30 dakika
        }
    }
}

# Application configuration
APP_CONFIG = {
    'debug': True,
    'host': '0.0.0.0',
    'port': int(os.getenv('PORT', 5000)),
    'log_level': 'INFO',
    'cors_origins': ['*']
} 