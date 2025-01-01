import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twitter API Configuration
TWITTER_CONFIG = {
    "API_KEY": os.getenv("TWITTER_API_KEY"),
    "API_KEY_SECRET": os.getenv("TWITTER_API_KEY_SECRET"),
    "BEARER_TOKEN": os.getenv("TWITTER_BEARER_TOKEN"),
    "ACCESS_TOKEN": os.getenv("TWITTER_ACCESS_TOKEN"),
    "ACCESS_TOKEN_SECRET": os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
}

# OpenAI Configuration
OPENAI_CONFIG = {
    "API_KEY": os.getenv("OPENAI_API_KEY"),
    'model': 'gpt-4',
    'max_tokens': 300,
    'temperature': 0.7
}

# Tavily API Configuration
TAVILY_CONFIG = {
    "API_KEY": os.getenv("TAVILY_API_KEY")
}

# Application Settings
APP_CONFIG = {
    'debug': True,
    'host': '0.0.0.0',
    'port': int(os.getenv('PORT', 5000))
}

# Expert System Configuration
EXPERT_CONFIG = {
    'sports': {
        'name': 'SportsExpert',
        'description': 'Sports and fitness expert',
        'openai': {
            'model': 'gpt-4',
            'max_tokens': 300,
            'temperature': 0.7
        }
    },
    'food': {
        'name': 'FoodExpert',
        'description': 'Food and cooking expert',
        'openai': {
            'model': 'gpt-4',
            'max_tokens': 300,
            'temperature': 0.7
        }
    },
    'ai': {
        'name': 'AIExpert',
        'description': 'AI and technology expert',
        'openai': {
            'model': 'gpt-4',
            'max_tokens': 300,
            'temperature': 0.7
        }
    },
    'sudostar': {
        'name': 'SudoStarExpert',
        'description': 'SudoStar app expert',
        'openai': {
            'model': 'gpt-4',
            'max_tokens': 300,
            'temperature': 0.7
        }
    },
    'general': {
        'name': 'GeneralExpert',
        'description': 'General knowledge expert',
        'openai': {
            'model': 'gpt-4',
            'max_tokens': 300,
            'temperature': 0.7
        }
    }
}

# System Messages
SYSTEM_MESSAGES = {
    'openai_prompt': "Sen profesyonel ve arkadaş canlısı bir asistansın. En fazla 3 kısa cümle kullanarak, özlü ve yararlı yanıtlar vermelisin. Emoji kullanabilirsin."
} 