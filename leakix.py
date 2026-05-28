import requests
import os
import dotenv
import json

from shodanIO import domain_to_ip

def leak(target):
    API_KEY = os.getenv('LEAKIX_KEY')
    
    if not API_KEY:
        print("Ошибка: LEAKIX_KEY не найден в файле .env")
        return False

    if any(c.isalpha() for c in target):
        try:
            ip = domain_to_ip(target)
        except Exception as e:
            print(f"Ошибка разрешения домена {target}: {e}")
            return False
    else:
        ip = target

    HEADERS = {
        "api-key": API_KEY, 
        "Accept": "application/json"
    }

    try:
        resp = requests.get(f"https://leakix.net/host/{ip}", headers=HEADERS, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, dict):
                services = data.get("Services", [])
            else:
                services = []
        elif resp.status_code == 404:
            services = []
        else:
            print(f"Ошибка LeakIX API: Статус-код {resp.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка подключения к leakix.net: {e}")
        return False
    except Exception as e:
        print(f"Непредвиденная ошибка в модуле leakix: {e}")
        return False

    return json.dumps(services, indent=2, ensure_ascii=False)