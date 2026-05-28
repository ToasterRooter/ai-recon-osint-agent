import requests
import json

IP_TOOLS = {
    "nmap_scan": "nmap",
    "reverse_ip": "reverseiplookup",
    "whois": "whois",
    "geoip": "geoip"
}

def call_ht_endpoint(endpoint_name, ip_target):
    url = f"https://api.hackertarget.com/{endpoint_name}/?q={ip_target}"
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            text = response.text.strip()
            if "api count exceeded" in text.lower():
                return "Ошибка: Превышен лимит бесплатных запросов к HackerTarget API."
            if "error" in text.lower():
                return f"Ошибка HackerTarget: {text}"
            return text
        else:
            return f"Ошибка сервера: статус {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Ошибка сетевого соединения: {e}"

def get_ip_intelligence(ip_target):
    ht_package = {}
    
    for key, endpoint in IP_TOOLS.items():
        print(f"    -> Опрос модуля: {key}...")
        raw_result = call_ht_endpoint(endpoint, ip_target)
        ht_package[key] = raw_result
        
    return json.dumps(ht_package, ensure_ascii=False)