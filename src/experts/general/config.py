"""General Expert için yapılandırma"""
from typing import Dict, Any
import os

def load_general_expert_config() -> Dict[str, Any]:
    """General expert için yapılandırma yükle"""
    return {
        'name': 'GeneralExpert',
        'description': 'Genel konularda uzman AI asistan',
        
        # OpenAI yapılandırması
        'openai': {
            'api_key': os.getenv('OPENAI_API_KEY'),
            'model': 'gpt-4',
            'max_tokens': 300,
            'temperature': 0.7
        },
        
        # AccuWeather yapılandırması
        'accuweather': {
            'api_key': os.getenv('ACCUWEATHER_API_KEY'),
            'language': 'tr-tr',
            'details': True
        },
        
        # News API yapılandırması
        'news': {
            'api_key': os.getenv('NEWS_API_KEY'),
            'country': 'tr',
            'language': 'tr'
        },
        
        # Yerel dosya yapılandırması
        'local': {
            'data_file': 'general_knowledge.json',
            'update_interval': 3600  # 1 saat
        },
        
        # URL yapılandırması
        'url': {
            'sources': [
                'https://www.tcmb.gov.tr',
                'https://api.accuweather.com',
                'https://newsapi.org'
            ],
            'update_interval': 300  # 5 dakika
        },
        
        # Tavily yapılandırması
        'tavily': {
            'api_key': os.getenv('TAVILY_API_KEY'),
            'max_results': 5,
            'search_depth': 'advanced'
        },
        
        # Bilgi kaynakları öncelikleri (0-1 arası)
        'source_weights': {
            'local': 0.4,    # Yerel bilgiler (tarih, saat vb.)
            'url': 0.3,      # API verileri (hava durumu, döviz vb.)
            'web': 0.2,      # Web araması
            'openai': 0.1    # AI tahminleri
        },
        
        # Önbellek yapılandırması
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