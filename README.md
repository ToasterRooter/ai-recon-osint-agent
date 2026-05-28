# AI-RECON OSINT AGENT

[Русский](#русский) | [English](#english)

---

## Русский

###  Описание проекта
**AI-RECON OSINT AGENT** — это мощный модульный инструмент для проведения пассивной разведки (OSINT) и Threat Intelligence защищенного периметра. Скрипт автоматизирует сбор данных об IP-адресах и доменах из пяти независимых аналитических платформ, агрегирует результаты в единый профиль и передает его интегрированному ИИ-агенту для глубокого экспертного анализа и интерактивного взаимодействия.

Архитектура построена по принципу модульной изоляции, что позволяет легко масштабировать систему, добавлять новые API-источники и настраивать поведение ИИ без изменения логики ядра.

### Ключевые возможности
* **Мультиплатформенный сбор данных (5-в-1):**
  * **Shodan / InternetDB:** Сведения об открытых портах, обнаруженных уязвимостях (CVE) и сетевой инфраструктуре.
  * **VirusTotal:** Репутационный анализ, вердикты антивирусных вендоров, поиск связанных доменов и поддоменов.
  * **AbuseIPDB:** Проверка истории вредоносной активности, спама, DDoS и оценка уровня доверия (Abuse Score).
  * **LeakIX:** Поиск открытых утечек, публично доступных конфигурационных файлов, баз данных и уязвимых сервисов.
  * **HackerTarget:** Удаленный запуск Nmap (сканирование стандартных портов), Reverse IPLookup (соседи по хостингу), Whois подсети и точная GeoIP-привязка.
* **ИИ-Аналитика на базе OpenRouter:** Автоматическая генерация комплексных ИБ-отчетов с категоризацией рисков (Низкий/Средний/Высокий/Критический) и пошаговым планом защиты.
* **Интерактивный ИИ-Чат:** Полноценный режим вопросов и ответов (Q&A) по собранным данным с удержанием контекста беседы (скользящее окно диалогов).
* **Отказоустойчивость:** Каждый модуль защищен блоками `try-except`, гарантируя стабильную работу комбайна даже при сетевых сбоях или исчерпании лимитов внешних API.
* **Автосохранение отчетов:** Сырые JSON-данные и аналитические отчеты ИИ автоматически сохраняются в директорию `reports/` с точными временными метками.

###  Архитектура проекта
Проект разделен на независимые функциональные модули:
* `main.py` — Управляющее ядро системы: интерактивное меню в стиле Metasploit, оркестрация API-запросов и файловый менеджер.
* `AIagent.py` — Движок взаимодействия с API OpenRouter (по умолчанию используется модель `nvidia/nemotron-3-super-120b-a12b:free`).
* `shodanIO.py` — Интеграция с Shodan API с резервным переключением на публичный InternetDB API.
* `virust.py` — Парсинг целей и взаимодействие с VirusTotal v3 API.
* `abuseipdb.py` — Репутационная проверка IP через AbuseIPDB API v2.
* `leakix.py` — Поиск утечек данных и уязвимостей через LeakIX API.
* `hackertarget.py` — Сбор данных о сетевой инфраструктуре через бесплатный API HackerTarget без использования токенов.

---

###  Установка и настройка

#### 1. Клонирование репозитория и установка зависимостей
```bash
# Клонируйте репозиторий
git clone [https://github.com/yourusername/ai-recon-osint-agent.git](https://github.com/yourusername/ai-recon-osint-agent.git)
cd ai-recon-osint-agent

# Установите необходимые библиотеки
pip install requests shodan openai python-dotenv

```

#### 2. Настройка переменных окружения

Создайте файл `.env` в корневой директории проекта и укажите ваши API-ключи:

```env
OPENROUTER_KEY=your_openrouter_api_key_here
SHODAN_KEY=your_shodan_api_key_here
VIRUSTOTAL_KEY=your_virustotal_api_key_here
ABUSEIPDB_KEY=your_abuseipdb_api_key_here
LEAKIX_KEY=your_leakix_api_key_here

```

---

### Использование

Запустите главный скрипт:

```bash
python main.py

```

#### Порядок работы:

1. В стартовом баннере отобразится статус готовности всех модулей.
2. В строке ввода `recon (enter target ip/domain) > ` укажите целевой IP-адрес или домен (домен автоматически разрешится в IP, где это необходимо).
3. Программа поочередно опросит все доступные источники данных.
4. Вы попадете во внутреннее **Меню управления результатами**:
* **Вариант 1:** Просмотр сырого агрегированного JSON-пакета данных и его автоматический экспорт в `reports/recon_[target]_raw_[timestamp].json`.
* **Вариант 2:** Генерация ИИ-экспертом структурированного ИБ-отчета (с сохранением в `reports/recon_[target]_ai_report_[timestamp].txt`).
* **Вариант 3:** Переход в режим живого чата с ИИ (`ai_chat_scout > `), где можно задавать любые уточняющие вопросы по уязвимостям. Для возврата в меню введите `back`.



---

---

## English

###  Project Description

**AI-RECON OSINT AGENT** is a highly modular passive reconnaissance (OSINT) and Threat Intelligence tool designed for external network perimeter evaluation. The script automates data harvesting from five independent security platforms, aggregates the multi-source findings into a unified target profile, and hooks into an integrated AI Analyst for deep expert reasoning and interactive exploration.

The architecture strictly adheres to modular isolation patterns, making it effortless to scale the system, onboard new API streams, or hot-swap AI models without altering the core operational logic.

###  Core Features

* **Multi-Source Intelligence Gathering (5-in-1):**
* **Shodan / InternetDB:** Maps open ports, protocol banners, and known CVE vulnerabilities.
* **VirusTotal:** Reputation forensics, antivirus vendor verdicts, passive DNS resolution, and subdomains lookup.
* **AbuseIPDB:** Cross-references history of malicious activities, spamming, and calculates the overall Abuse Score.
* **LeakIX:** Uncovers open leaks, exposed configuration files, misconfigured databases, and vulnerable web services.
* **HackerTarget:** Remotely orchestrates safe Nmap scans (top standard TCP ports), Reverse IP mapping (shared hosting neighbors), WHOIS block lookups, and exact GeoIP geolocation.


* **AI-Powered Analytics via OpenRouter:** Automatically formats gathered footprints into actionable cybersecurity reports featuring risk grading (Low/Medium/High/Critical) and detailed remediation playbooks.
* **Interactive AI Chat:** Implements a context-aware chat environment (`ai_chat_scout > `) dedicated to target analysis, retaining short-term conversation memory through a sliding dialog window.
* **Fault Tolerance:** Every API caller is safely nested inside dedicated `try-except` blocks, ensuring the main application keeps running seamlessly even if individual remote services timeout or hit rate-limits.
* **Automated Report Logging:** All structural raw responses and generated AI text reports are cleanly saved into the local `reports/` directory with explicit timestamps.

###  Directory Blueprint

The codebase is separated into singular, decoupled components:

* `main.py` — Orchestration Core: provides the Metasploit-inspired CLI interface, routes data payloads, and handles file persistence.
* `AIagent.py` — LLM Communication Engine: connects to the OpenRouter endpoint (utilizes `nvidia/nemotron-3-super-120b-a12b:free` by default).
* `shodanIO.py` — Shodan API bridge featuring a fallback pipeline to the public InternetDB endpoint.
* `virust.py` — Handles input parsing and extracts detection trees from VirusTotal v3.
* `abuseipdb.py` — Queries IP threat reputation datasets via AbuseIPDB v2.
* `leakix.py` — Checks for exposed intelligence leaks using the LeakIX engine.
* `hackertarget.py` — Harnesses open server-side network utilities from HackerTarget without token dependencies.

---

###  Installation & Setup

#### 1. Clone the Repository & Fetch Dependencies

```bash
# Clone this repository
git clone [https://github.com/yourusername/ai-recon-osint-agent.git](https://github.com/yourusername/ai-recon-osint-agent.git)
cd ai-recon-osint-agent

# Install mandatory libraries
pip install requests shodan openai python-dotenv

```

#### 2. Environment Configuration

Create a `.env` file in the root directory of the project and populate it with your personal API credentials:

```env
OPENROUTER_KEY=your_openrouter_api_key_here
SHODAN_KEY=your_shodan_api_key_here
VIRUSTOTAL_KEY=your_virustotal_api_key_here
ABUSEIPDB_KEY=your_abuseipdb_api_key_here
LEAKIX_KEY=your_leakix_api_key_here

```

---

###  Usage Instruction

Fire up the terminal script:

```bash
python main.py

```

#### Workflow Overview:

1. The terminal banner boots up, verifying the loading sequence of your security modules.
2. Provide a domain name or IP target at the console prompt: `recon (enter target ip/domain) > ` (The tool seamlessly executes DNS lookups internally where applicable).
3. The aggregator fetches structural data packets asynchronously across all endpoints.
4. You enter the interactive **Session Results Management Menu**:
* **Option 1:** Inspect the aggregate raw JSON tree and automatically export it to `reports/recon_[target]_raw_[timestamp].json`.
* **Option 2:** Instruct the AI Analyst to compile an expert security audit, saved to `reports/recon_[target]_ai_report_[timestamp].txt`.
* **Option 3:** Jump into the continuous AI conversation room to interrogate the agent regarding specific vulnerabilities. Enter `back` to return to the option matrix.



```

```
