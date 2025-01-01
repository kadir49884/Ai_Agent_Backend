"""General Expert için arama sorguları"""

SEARCH_TEMPLATES = {
    "weather": {
        "current": "{city} hava durumu bugün",
        "forecast": "{city} hava durumu {days} günlük",
        "detail": "{city} sıcaklık nem rüzgar",
        "alert": "{city} hava durumu uyarısı"
    },
    "exchange": {
        "currency": "{currency} kuru kaç TL",
        "compare": "{currency1}/{currency2} paritesi",
        "trend": "{currency} kuru son durum",
        "forecast": "{currency} kuru tahmin"
    },
    "news": {
        "latest": "{topic} son dakika haberleri",
        "summary": "{topic} gündem özeti",
        "analysis": "{topic} detaylı analiz",
        "local": "{city} yerel haberler"
    },
    "traffic": {
        "current": "{city} trafik durumu",
        "route": "{start} {end} trafik",
        "incident": "{location} yol durumu",
        "parking": "{location} otopark durumu"
    },
    "event": {
        "today": "{city} bugün etkinlikler",
        "upcoming": "{city} yaklaşan etkinlikler",
        "category": "{city} {category} etkinlikleri",
        "venue": "{venue} program"
    }
}

def get_search_query(category: str, template: str, **kwargs) -> str:
    """Arama sorgusu oluştur"""
    query_template = SEARCH_TEMPLATES.get(category, {}).get(template)
    if query_template:
        return query_template.format(**kwargs)
    return None 