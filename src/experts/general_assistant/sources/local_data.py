"""General Expert için yerel veri kaynakları"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

# Sık sorulan sorular ve yanıtları
COMMON_QUESTIONS = {
    "tarih": {
        "bugün": lambda: datetime.now().strftime("%d %B %Y %A"),
        "yarın": lambda: (datetime.now() + timedelta(days=1)).strftime("%d %B %Y %A"),
        "dün": lambda: (datetime.now() - timedelta(days=1)).strftime("%d %B %Y %A")
    },
    "saat": {
        "şimdi": lambda: datetime.now().strftime("%H:%M"),
        "timestamp": lambda: datetime.now().timestamp()
    }
}

# Şehir bilgileri
CITIES = {
    "istanbul": {
        "id": "istanbul",
        "name": "İstanbul",
        "region": "Marmara",
        "weather_id": "318251",
        "timezone": "Europe/Istanbul"
    },
    "ankara": {
        "id": "ankara",
        "name": "Ankara",
        "region": "İç Anadolu",
        "weather_id": "316938",
        "timezone": "Europe/Istanbul"
    },
    "izmir": {
        "id": "izmir",
        "name": "İzmir",
        "region": "Ege",
        "weather_id": "311046",
        "timezone": "Europe/Istanbul"
    }
}

# Para birimleri
CURRENCIES = {
    "usd": {"name": "Amerikan Doları", "symbol": "$"},
    "eur": {"name": "Euro", "symbol": "€"},
    "gbp": {"name": "İngiliz Sterlini", "symbol": "£"},
    "try": {"name": "Türk Lirası", "symbol": "₺"}
}

def get_city_info(city_name: str) -> Optional[Dict[str, Any]]:
    """Şehir bilgilerini getir"""
    return CITIES.get(city_name.lower())

def get_currency_info(currency_code: str) -> Optional[Dict[str, Any]]:
    """Para birimi bilgilerini getir"""
    return CURRENCIES.get(currency_code.lower())

def get_common_answer(category: str, query: str) -> Optional[str]:
    """Sık sorulan sorulara yanıt ver"""
    if category in COMMON_QUESTIONS and query in COMMON_QUESTIONS[category]:
        return COMMON_QUESTIONS[category][query]()
    return None 