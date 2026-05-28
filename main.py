import os
import sys
import json
import dotenv

from AIagent import agent

from shodanIO import get_shodan, domain_to_ip
from virust import virtot
from abuseipdb import check_ip
from leakix import leak
from hackertarget import get_ip_intelligence

R = "\033[31m"
G = "\033[32m"
Y = "\033[33m"
B = "\033[34m"
CYAN = "\033[36m"
RESET = "\033[0m"

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = fr"""{B}
      ___           ___           ___           ___       ___           ___     
     /\  \         /\  \         /\  \         /\__\     /\  \         /\__\    
    /::\  \       /::\  \       /::\  \       /:/  /    /::\  \       /:/ _/_   
   /:/\:\  \     /:/\:\  \     /:/\:\  \     /:/  /    /:/\:\  \     /:/ /\__\  
  /::\~\:\  \   /::\~\:\  \   /:/  \:\  \   /:/  /    /::\~\:\  \   /:/ /:/ _/_ 
 /:/\:\ \:\__\ /:/\:\ \:\__\ /:/__/ \:\__\ /:/__/    /:/\:\ \:\__\ /:/_/:/ /\__\
 \/__\:\/:/  / \:\~\:\ \/__/ \:\  \  \/__/ \:\  \    \:\~\:\ \/__/ \:\/:/ /:/  /
      \::/  /   \:\ \:\__\    \:\  \        \:\  \    \:\ \:\__\    \::/_/:/  / 
      /:/  /     \:\/:/  /     \:\__\        \:\  \    \:\/:/  /     \:\/:/  /  
     /:/  /       \::/  /       \:\__\        \:\__\    \::/  /       \::/  /   
     \/__/         \/__/         \/__/         \/__/     \/__/         \/__/    
                               AI-RECON OSINT AGENT{RESET}"""
    print(banner)
    print(f"{Y} [*] Модули загружены: Shodan [OK] | VirusTotal [OK] | AbuseIPDB [OK] | HackerTarget [OK] | Leakix [OK] {RESET}")
    print(f"{G} [+] Введите 'exit' или 'quit' для выхода из программы.{RESET}\n")

def make_context(set_role, set_content):
    return {'role': set_role, 'content': set_content}

def collect_all_data(target):
    print(f"\n{Y}[*] Начало сбора данных для: {target}{RESET}")
    
    clean_ip = target
    if not any(char.isdigit() for char in target):
        try:
            print(f"{Y}[*] Обнаружен домен. Резолвим в IP...{RESET}")
            clean_ip = domain_to_ip(target)
            print(f"{G}[+] IP успешно определен: {clean_ip}{RESET}")
        except Exception as e:
            print(f"{R} [-] Ошибка DNS-резолвинга: {e}{RESET}")

    print(f"{Y}[*] Запрос данных из Shodan/InternetDB...{RESET}")
    try:
        shodan_raw = get_shodan(target)
        shodan_json = json.loads(shodan_raw) if shodan_raw else {"error": "Нет данных от Shodan"}
    except Exception as e:
        print(f"{R} [-] Ошибка при вызове Shodan: {e}{RESET}")
        shodan_json = {"error": f"Исключение при вызове Shodan: {e}"}


    print(f"{Y}[*] Запрос данных из VirusTotal...{RESET}")
    try:
        vt_raw = virtot(target)
        vt_json = json.loads(vt_raw) if vt_raw else {"error": "Нет данных от VirusTotal"}
    except Exception as e:
        print(f"{R} [-] Ошибка при вызове VT: {e}{RESET}")
        vt_json = {"error": f"Исключение при вызове VT: {e}"}

    print(f"{Y}[*] Запрос данных из AbuseIPDB...{RESET}")
    try:
        abuse_raw = check_ip(clean_ip)
        abuse_json = json.loads(abuse_raw) if abuse_raw else {"error": "Нет данных от AbuseIPDB"}
    except Exception as e:
        print(f"{R} [-] Ошибка при вызове AbuseIPDB: {e}{RESET}")
        abuse_json = {"error": f"Исключение при вызове AbuseIPDB: {e}"}        

    print(f"{Y}[*] Запрос данных из Leakix...{RESET}")
    try:
        leakix_raw = leak(clean_ip)
        leakix_json = json.loads(leakix_raw) if leakix_raw else {"error": "Нет данных от Leakix"}
    except Exception as e:
        print(f"{R} [-] Ошибка при вызове Leakix: {e}{RESET}")
        leakix_json = {"error": f"Исключение при вызове Leakix: {e}"}           

    print(f"{Y}[*] Запрос данных из HackerTarget...{RESET}")
    try:
        hackertarget_raw = get_ip_intelligence(clean_ip)
        hackertarget_json = json.loads(hackertarget_raw) if hackertarget_raw else {"error": "Нет данных от HackerTarget"} 
    except Exception as e:
        print(f"{R} [-] Ошибка при вызове HackerTarget: {e}{RESET}")
        hackertarget_json = {"error": f"Исключение при вызове HackerTarget: {e}"}  

    aggregated_data = {
        "target": target,
        "resolved_ip": clean_ip,
        "shodan_data": shodan_json,
        "virustotal_data": vt_json,
        "abuseipdb_data": abuse_json,
        "leakix_data": leakix_json,
        "hackertarget": hackertarget_json
    }
    
    print(f"{G}[+] Сбор данных успешно завершен!{RESET}")
    return aggregated_data

def start_ai_chat(aggregated_data_str):
    print(f"\n{CYAN}=== РЕЖИМ ИНТЕРАКТИВНОГО ЧАТА С ИИ ==={RESET}")
    print(f"{CYAN}ИИ видит все собранные данные. Задавайте любые вопросы (например, 'какие порты самые опасные?', 'что делать с CVE-XXXX').{RESET}")
    print(f"{CYAN}Для выхода из чата обратно в меню введите 'back'.{RESET}\n")
    
    system_prompt = (
        "Ты — эксперт по кибербезопасности и Threat Intelligence. Пользователь собрал данные по хосту "
        "и хочет обсудить их с тобой в формате чата. Отвечай на его вопросы, опираясь строго на предоставленный "
        "ниже JSON. Давай профессиональные, но понятные советы по защите.\n\n"
        f"ДАННЫЕ ОБЪЕКТА:\n{aggregated_data_str}"
    )
    
    chat_context = system_prompt
    
    while True:
        user_query = input(f"{CYAN}ai_chat_scout > {RESET}").strip()
        if not user_query:
            continue
        if user_query.lower() == 'back':
            print(f"{CYAN}[*] Выход из режима чата.{RESET}")
            break
            
        print(f"{Y}[*] ИИ думает...{RESET}")
        ai_response = agent(chat_context, user_query)
        
        print(f"\n{G}[ИИ]:{RESET} {ai_response}\n")
        
        chat_context += f"\nПользователь спрашивал: {user_query}\nТы отвечал: {ai_response}"

def run_session_menu(aggregated_data):
    data_str = json.dumps(aggregated_data, indent=2, ensure_ascii=False)
    
    while True:
        print(f"\n--- МЕНЮ УПРАВЛЕНИЯ РЕЗУЛЬТАТАМИ ({aggregated_data['target']}) ---")
        print("1. Посмотреть весь сырой JSON (чистый str/json от всех функций)")
        print("2. Получить финальный структурированный отчет от ИИ-Аналитика")
        print("3. Войти в режим интерактивного ЧАТА с ИИ по этим данным")
        print("4. Сканировать новую цель (Вернуться назад)")
        print("5. Выйти из программы")
        
        choice = input(f"\n{R}msf_recon(action) > {RESET}").strip()
        
        if choice == '1':
            print(f"\n{G}=== СЫРЫЕ ДАННЫЕ (AGREAGATED JSON) ==={RESET}\n")
            print(data_str)
            print(f"\n{G}======================================{RESET}\n")
            
        elif choice == '2':
            print(f"\n{Y}[*] ИИ генерирует комплексный аналитический отчет, подождите...{RESET}")
            system_prompt_analyst = (
                "Ты — ИИ-агент «Разведчик сетевого периметра», ведущий эксперт по кибербезопасности.\n"
                "Перед тобой агрегированные данные из Shodan, HackerTarget, VirusTotal, Leakix.net и AbuseIPDB. Твоя задача — сопоставить их и выдать глубокий экспертный отчет.\n\n"
                "Формат ответа (строго):\n"
                "1. **Общая информация**: IP, домен, гео-данные, провайдер.\n"
                "2. **Архитектура сети**: Открытые порты, какие сервисы и версии на них крутятся.\n"
                "3. **Анализ угроз и репутации (VT + AbuseIPDB)**: Есть ли детекты вредоносной активности, какой Abuse Score, какие поддомены или связанные сайты обнаружены.\n"
                "4. **Уязвимости и Оценка риска**: Перечень CVE (если есть), оценка риска (низкий/средний/высокий/критический) с жестким обоснованием.\n"
                "5. **Рекомендации по защите**: Пошаговый план, как закрыть дыры.\n\n"
                "Будь точен, не придумывай факты. Пиши профессионально."
            )
            report = agent(system_prompt_analyst, data_str)
            print(f"\n{G}=== КОМПЛЕКСНЫЙ ОТЧЕТ ИИ-АНАЛИТИКА ==={RESET}\n")
            print(report)
            print(f"\n{G}======================================{RESET}\n")
            
        elif choice == '3':
            start_ai_chat(data_str)
            
        elif choice == '4':
            print(f"{Y}[*] Возврат в главное меню...{RESET}")
            break
            
        elif choice == '5' or choice.lower() in ['exit', 'quit']:
            print(f"{G}[*] Завершение сессии. До свидания!{RESET}")
            sys.exit(0)
        else:
            print(f"{R}[-] Неверный пункт меню. Попробуйте снова.{RESET}")

def main():
    dotenv.load_dotenv()
    
    if not os.getenv('OPENROUTER_KEY'):
        print(f"{R}Критическая ошибка: OPENROUTER_KEY не найден в файле .env!{RESET}")
        sys.exit(1)

    while True:
        print_banner()
        target = input(f"{R}recon (enter target ip/domain) > {RESET}").strip()
        
        if not target:  
            continue
            
        if target.lower() in ['exit', 'quit']:
            print(f"{G}[*] Выход из программы.{RESET}")
            break
            
        try:
            data_package = collect_all_data(target)
            
            run_session_menu(data_package)
            
        except KeyboardInterrupt:
            print(f"\n{Y}[*] Процесс прерван. Возврат в главное меню.{RESET}")
        except Exception as e:
            print(f"{R}[-] Ошибка в главном модуле: {e}{RESET}")
            input("\nНажмите Enter для продолжения...")

if __name__ == '__main__':
    main()