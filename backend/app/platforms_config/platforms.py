"""Configuration des plateformes de scraping"""

SUPPORTED_PLATFORMS = {
    "indeed": {"name": "Indeed", "base_url": "https://fr.indeed.com", "enabled": False},
    "welcometothejungle": {"name": "WTTJ", "base_url": "https://www.welcometothejungle.com", "enabled": False},
    "remoteok": {"name": "RemoteOK", "base_url": "https://remoteok.com", "enabled": True},
    "adzuna": {"name": "Adzuna", "base_url": "https://www.adzuna.fr", "enabled": True},  # API avec demo keys
    "themuse": {"name": "The Muse", "base_url": "https://www.themuse.com", "enabled": True},
    "jsearch": {"name": "JSearch", "base_url": "https://jsearch.p.rapidapi.com", "enabled": True},  # Nécessite clé RapidAPI
}

def get_enabled_platforms():
    return {n: c for n, c in SUPPORTED_PLATFORMS.items() if c.get("enabled")}

def get_platform_config(name):
    return SUPPORTED_PLATFORMS.get(name, {})

def is_platform_enabled(name):
    return SUPPORTED_PLATFORMS.get(name, {}).get("enabled", False)
