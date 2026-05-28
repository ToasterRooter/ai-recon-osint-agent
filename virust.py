import json
import os
import requests
import dotenv

from AIagent import agent

def virtot(target):
    system_prompt_parser = (
        "Ты — парсер для VirusTotal API. Твоя задача: определить тип входных данных.\n"
        "1. Если передан IP-адрес (н-р, 8.8.8.8) -> верни строго строку: ip_addresses/<ip>\n"
        "2. Если передан домен (н-р, google.com) -> верни строго строку: domains/<домен>\n"
        "Отвечай ТОЛЬКО этой строкой, БЕЗ косых черт '/' в начале, без кавычек, пробелов и пояснений."
    )

    api_endpoint = agent(system_prompt_parser, target).strip()
    
    VIRUSTOTAL_API_KEY = os.getenv('VIRUSTOTAL_KEY')
    if not VIRUSTOTAL_API_KEY:
        print("Ошибка: Не найден VIRUSTOTAL_KEY в .env")
        return False

    url = f"https://www.virustotal.com/api/v3/{api_endpoint}"
    headers = {
        "x-apikey": VIRUSTOTAL_API_KEY,
        "accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Ошибка VirusTotal API: Статус {response.status_code}")
            return False

        raw_data = response.json()
        vt_attributes = raw_data.get('data', {}).get('attributes', {})

        analysis_results = vt_attributes.get('last_analysis_results', {})
        filtered_results = {
            vendor: details for vendor, details in analysis_results.items()
            if details.get('category') in ['malicious', 'suspicious']
        }
        vt_attributes['last_analysis_results'] = filtered_results

        relation = "resolutions" if "ip_addresses" in api_endpoint else "subdomains"
        rel_url = f"{url}/{relation}?limit=20"
        
        rel_response = requests.get(rel_url, headers=headers)
        if rel_response.status_code == 200:
            rel_data = rel_response.json().get('data', [])
            additional_info = []

            if relation == "resolutions":
                for obj in rel_data:
                    attrs = obj.get('attributes', {})
                    additional_info.append({
                        "host_name": attrs.get('host_name'),
                        "date": attrs.get('date')
                    })
                vt_attributes['connected_domains'] = additional_info
            else:
                for obj in rel_data:
                    additional_info.append(obj.get('id'))
                vt_attributes['discovered_subdomains'] = additional_info

        return json.dumps(vt_attributes, indent=2, ensure_ascii=False)

    except Exception as e:
        print(f"Непредвиденная ошибка при запросе к VT: {e}")
        return False