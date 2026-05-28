import json
import os
import requests
import dotenv

from shodanIO import domain_to_ip
from AIagent import agent

def check_ip(target):
    if isinstance(target, str):
        ip = domain_to_ip(target)
    else:
        ip = target

    dotenv.load_dotenv()
    API_KEY = os.getenv('ABUSEIPDB_KEY')

    url = 'https://api.abuseipdb.com/api/v2/check'

    headers = {
        'Accept': 'application/json',
        'Key': API_KEY
    }

    querystring = {
            'ipAddress': ip,
            'maxAgeInDays': '360',
            'verbose': True
        }
    
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        
        if response.status_code == 200:
            raw_data = response.json()
            abuse_attributes = raw_data.get('data', {})
            
            if 'reports' in abuse_attributes:
                abuse_attributes['reports'] = abuse_attributes['reports'][:5]
                
        else:
            print(f"Ошибка AbuseIPDB API: Статус-код {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Непредвиденная ошибка при обращении к AbuseIPDB: {e}")
        return False

    data_str = json.dumps(abuse_attributes, indent=2, ensure_ascii=False)
    return data_str