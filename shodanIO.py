import json
import shodan
import os
import dotenv
import socket
import requests

from AIagent import agent

def domain_to_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.gaierror:
        raise ValueError(f"Не удалось разрешить домен {domain}")

def get_ip_data(shodan_api, ip):
    try:
        return shodan_api.host(ip)
    except shodan.APIError as e:
        if '403' in str(e):
            print(f"Информация: нет прав для Shodan API, используем InternetDB API для {ip}.")
            try:
                response = requests.get(f"https://internetdb.shodan.io/{ip}", timeout=10)
                if response.status_code == 200:
                    internetdb_data = response.json()
                    compatible_data = {
                        'ip_str': ip,
                        'data': internetdb_data,
                        'ports': internetdb_data.get('ports', []),
                        'vulns': internetdb_data.get('vulns', {})
                    }
                    return compatible_data
                else:
                    print(f"Данные для {ip} не найдены в InternetDB.")
            except Exception as ie:
                print(f"Ошибка при запросе к InternetDB: {ie}")
        raise e

def get_shodan(target):

    system_prompt = (
        "Ты — парсер запросов к Shodan API. Твоя задача: проанализировать сообщение пользователя "
        "и вернуть ТОЛЬКО валидный JSON-объект для вызова Shodan API.\n\n"
        "Правила:\n"
        "1. Если пользователь указал IP-адрес (например, '8.8.8.8', '192.168.1.1') → "
        "{\"action\": \"host\", \"ip\": \"<IP>\"}\n"
        "2. Если пользователь указал домен (например, 'google.com', 'dwg.ru') → "
        "{\"action\": \"search\", \"query\": \"hostname:<домен>\"}\n"
        "3. Если пользователь указал страну (Россия, США, Германия, UK и т.д.) → "
        "преобразуй в код страны (RU, US, DE, GB) и верни {\"action\": \"search\", \"query\": \"country:<код>\"}\n"
        "4. Если пользователь указал город (Москва, Лондон, Берлин) → "
        "{\"action\": \"search\", \"query\": \"city:\\\"<город на английском>\\\"\"}\n"
        "5. Если пользователь указал порт ('порт 22', 'port 443', '22 порт') → "
        "добавь в search-запрос фильтр port:<номер>\n"
        "6. Если несколько критериев (например, 'Россия порт 80') → объедини через пробел: "
        "{\"action\": \"search\", \"query\": \"country:RU port:80\"}\n"
        "7. Если только ключевое слово без фильтров ('nginx', 'webcam', 'apache') → "
        "{\"action\": \"search\", \"query\": \"<слово>\"}\n"
        "8. Если запрос не распознан → {\"action\": \"error\", \"message\": \"Не понял запрос. Примеры: '8.8.8.8', 'Россия', 'порт 22', 'dwg.ru'\"}\n\n"
        "9. Если пользователь указал подсеть (например, '8.8.8.0/24') → {\"action\": \"search\", \"query\": \"net:<подсеть>\"}\n"
        "Примеры:\n"
        "Ввод: '8.8.8.8' → {\"action\": \"host\", \"ip\": \"8.8.8.8\"}\n"
        "Ввод: 'google.com' → {\"action\": \"search\", \"query\": \"hostname:google.com\"}\n"
        "Ввод: 'Россия' → {\"action\": \"search\", \"query\": \"country:RU\"}\n"
        "Ввод: 'Москва' → {\"action\": \"search\", \"query\": \"city:\\\"Moscow\\\"\"}\n"
        "Ввод: 'США порт 443' → {\"action\": \"search\", \"query\": \"country:US port:443\"}\n"
        "Ввод: 'nginx' → {\"action\": \"search\", \"query\": \"nginx\"}\n"
        "Ввод: 'dwg.ru' → {\"action\": \"search\", \"query\": \"hostname:dwg.ru\"}\n"
        "Ввод: 'порт 22 Россия' → {\"action\": \"search\", \"query\": \"port:22 country:RU\"}\n"
        "Ввод: 'атака' → {\"action\": \"error\", \"message\": \"Не понял запрос. Примеры: '8.8.8.8', 'Россия', 'порт 22', 'dwg.ru'\"}\n\n"
        "Важно: Никаких пояснений, только чистый JSON на одной строке. Не придумывай лишнего."
    )

    user_promt = target

    json_for_shodan = agent(system_prompt, user_promt)

    SHODAN_API_KEY = os.getenv('SHODAN_KEY')
    shodan_api = shodan.Shodan(SHODAN_API_KEY)

    try:
        clean_json = json_for_shodan.replace("```json", "").replace("```", "").strip()
        params = json.loads(clean_json)
    except json.JSONDecodeError:
        return False
    action = params.get('action')
    query = params.get('query', '')
    shodan_result = None

    if action == 'search' and 'hostname:' in query:
        domain = query.split('hostname:')[-1].strip()
        
        try:
            ip = domain_to_ip(domain)
            action = 'host'
            params['ip'] = ip

        except ValueError as e:
            print(f"Ошибка: {e}")
            return False

    try:
        if action == 'host':
            ip = params.get('ip')
            if not ip:
                raise ValueError("Не указан IP-адрес для host-запроса")
            shodan_result = get_ip_data(shodan_api, ip)
            print(f"Shodan: успешно получены данные по хосту {ip}")

        elif action == 'search':
            print("Ошибка: Глобальный поиск (по портам/странам) недоступен в бесплатной версии API. Укажите IP или домен.")
            return False
        
        elif action == 'error':
            print(params.get('message', 'Ошибка распознавания запроса'))
            return False
        
        else:
            print(f"Неизвестное действие: {action}")
            return False

    except shodan.APIError as e:
        print(f"Ошибка Shodan API: {e}")
        shodan_result = None
    except Exception as e:
        print(f"Непредвиденная ошибка при обращении к Shodan: {e}")
        shodan_result = None

    if shodan_result is None:
        print("Не удалось получить данные от Shodan. Проверьте API-ключ или лимиты.")
        return False

    shodan_data_str = json.dumps(shodan_result, indent=2, ensure_ascii=False)
    return shodan_data_str