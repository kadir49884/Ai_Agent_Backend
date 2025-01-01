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
        'name': 'GeneralExpert',
        'description': 'Genel konularda uzman AI asistan',
        'openai': {
            'model': 'gpt-4',
            'max_tokens': 300,
            'temperature': 0.7
        },
        'accuweather': {
            'api_key': os.getenv('ACCUWEATHER_API_KEY'),
            'language': 'tr-tr',
            'details': True
        },
        'news': {
            'api_key': os.getenv('NEWS_API_KEY'),
            'country': 'tr',
            'language': 'tr'
        },
        'cache': {
            'enabled': True,
            'ttl': {
                'weather': 1800,     # 30 dakika
                'exchange': 300,     # 5 dakika
                'news': 600,        # 10 dakika
                'traffic': 300,     # 5 dakika
                'events': 3600      # 1 saat
            }
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