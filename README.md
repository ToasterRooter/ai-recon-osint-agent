# AI-RECON OSINT AGENT

[Русский](#русский) | [English](#english)

---

## Русский

### Описание проекта
**AI-RECON OSINT AGENT** — это модульный инструмент для проведения пассивной разведки (OSINT) и Threat Intelligence внешнего периметра. Скрипт автоматизирует сбор данных об IP-адресах и доменах из пяти независимых аналитических платформ, агрегирует результаты в единый профиль и передает его интегрированному ИИ-агенту для глубокого экспертного анализа и интерактивного взаимодействия в режиме реального времени.

Архитектура построена по принципу модульной изоляции (низкая связанность кода), что позволяет легко масштабировать систему, добавлять новые API-источники и настраивать поведение ИИ без изменения логики ядра.

### Ключевые возможности
* **Мультиплатформенный сбор данных (5-в-1):**
  * **Shodan / InternetDB:** Сведения об открытых портах, протоколах и обнаруженных уязвимостях (CVE).
  * **VirusTotal:** Репутационный анализ, вердикты антивирусных вендоров, пассивный DNS и поиск поддоменов.
  * **AbuseIPDB:** Проверка истории вредоносной активности (спам, DDoS, брутфорс) и оценка уровня доверия (Abuse Score).
  * **LeakIX:** Поиск публичных утечек данных, открытых конфигурационных файлов, баз данных и уязвимых веб-служб.
  * **HackerTarget:** Сетевой аудит без использования токенов (быстрый Nmap, Reverse IP, Whois подсети и GeoIP).
* **ИИ-Аналитика на базе OpenRouter:** Автоматическая генерация комплексных ИБ-отчетов с категоризацией рисков (Низкий/Средний/Высокий/Критический) и пошаговым планом митигации угроз.
* **Интерактивный ИИ-Чат:** Полноценный контекстно-зависимый режим вопросов и ответов (Q&A) по собранным данным через механизм скользящего окна диалогов.
* **Высокая отказоустойчивость:** Каждый модуль изолирован блоками `try-except`, что гарантирует стабильную работу комбайна даже при сбоях или таймаутах отдельных внешних API.
* **Автосохранение отчетов:** Результаты сканирования (сырой JSON) и аналитические отчеты ИИ автоматически сохраняются в структурированную директорию `reports/`.

### Структура репозитория
* `main.py` — Управляющее ядро системы: интерактивное CLI-меню в стиле Metasploit, оркестрация запросов и менеджер отчетов.
* `AIagent.py` — Движок взаимодействия с API OpenRouter (использует модель `nvidia/nemotron-3-super-120b-a12b:free`).
* `shodanIO.py` — Интеграция с Shodan API и отказоустойчивое переключение на публичный InternetDB API.
* `virust.py` — Интеллектуальный парсинг целей и взаимодействие с VirusTotal v3 API.
* `abuseipdb.py` — Модуль репутационной проверки хостов через AbuseIPDB API v2.
* `leakix.py` — Модуль поиска утечек и уязвимостей через LeakIX API.
* `hackertarget.py` — Модуль сбора сетевой инфраструктуры через бесплатный API HackerTarget.
* `requirements.txt` — Список внешних зависимостей и библиотек, необходимых для работы проекта.
* `.env` — Файл конфигурации переменных окружения (API-ключи).

---

### Установка и настройка

#### 1. Клонирование репозитория и установка зависимостей
Склонируйте репозиторий и установите все необходимые библиотеки одной командой с помощью `requirements.txt`:
```bash
git clone https://github.com/ToasterRooter/ai-recon-osint-agent.git
cd ai-recon-osint-agent

# Автоматическая установка всех зависимостей
pip install -r requirements.txt

```

#### 2. Настройка переменных окружения

Откройте файл `.env` в корневой директории проекта и укажите ваши API-ключи:

```env
OPENROUTER_KEY=your_openrouter_api_key_here
SHODAN_KEY=your_shodan_api_key_here
VIRUSTOTAL_KEY=your_virustotal_api_key_here
ABUSEIPDB_KEY=your_abuseipdb_api_key_here
LEAKIX_KEY=your_leakix_api_key_here

```

---

### Инструкция по использованию

Запустите главный скрипт программы:

```bash
python main.py

```

#### Порядок работы:

1. При запуске отобразится интерактивный баннер и проверится статус модулей.
2. В строке ввода `recon (enter target ip/domain) > ` укажите целевой IP-адрес или домен.
3. Программа поочередно опросит все доступные API.
4. Вы попадете во внутреннее **Меню управления результатами**:
* **Вариант 1:** Просмотр сырого агрегированного JSON-пакета данных и его экспорт в `reports/recon_[target]_raw_[timestamp].json`.
* **Вариант 2:** Генерация ИИ-экспертом структурированного ИБ-отчета с сохранением в `reports/recon_[target]_ai_report_[timestamp].txt`.
* **Вариант 3:** Переход в режим живого чата с ИИ (`ai_chat_scout > `) для детализации уязвимостей (введите `back` для возврата в меню).

---

---

## English

### Project Description

**AI-RECON OSINT AGENT** is a modular passive reconnaissance (OSINT) and Threat Intelligence tool designed for external network perimeter evaluation. The script automates data harvesting from five independent security and analysis platforms, aggregates the multi-source findings into a unified target profile, and hooks into an integrated AI Analyst for deep expert reasoning and interactive exploration.

The architecture strictly adheres to modular isolation patterns (low coupling), making it effortless to scale the system, onboard new API streams, or hot-swap AI models without altering the core operational logic.

### Core Features

* **Multi-Source Intelligence Gathering (5-in-1):**
* **Shodan / InternetDB:** Maps open ports, protocol banners, and known CVE vulnerabilities.
* **VirusTotal:** Reputation forensics, antivirus vendor verdicts, passive DNS domain resolution, and subdomains lookup.
* **AbuseIPDB:** Cross-references history of malicious activities (spam, DDoS, brute-forcing) and calculates the overall Abuse Score.
* **LeakIX:** Uncovers open leaks, exposed configuration files, misconfigured databases, and internet-facing vulnerable web services.
* **HackerTarget:** Remotely orchestrates safe network utilities (Nmap top ports, Reverse IP mapping, WHOIS subnets, and exact GeoIP).


* **AI-Powered Analytics via OpenRouter:** Automatically formats gathered footprints into actionable cyber security reports featuring risk grading (Low/Medium/High/Critical) and detailed remediation playbooks.
* **Interactive AI Chat:** Implements a context-aware chat environment (`ai_chat_scout > `) dedicated to target analysis, retaining short-term conversation memory through a sliding dialog window.
* **Fault Tolerance:** Every API caller is safely nested inside dedicated `try-except` sandboxes, ensuring the main application keeps running seamlessly even if individual remote services timeout or hit rate-limits.
* **Automated Report Logging:** All structural raw responses and generated AI text reports are cleanly persisted into the local `reports/` directory with explicit timestamps.

### Repository Structure

* `main.py` — Orchestration Core: provides the Metasploit-inspired CLI interface, routes data payloads, and handles file persistence.
* `AIagent.py` — LLM Communication Engine: connects to the OpenRouter endpoint (utilizes `nvidia/nemotron-3-super-120b-a12b:free` by default).
* `shodanIO.py` — Shodan API bridge featuring a fallback pipeline to the public InternetDB endpoint.
* `virust.py` — Handles conditional input parsing and extracts detection trees from VirusTotal v3.
* `abuseipdb.py` — Queries IP threat reputation datasets via AbuseIPDB v2.
* `leakix.py` — Checks for exposed intelligence leaks using the LeakIX engine.
* `hackertarget.py` — Harnesses open server-side network utilities from HackerTarget without token dependencies.
* `requirements.txt` — List of external dependencies and libraries required for the project.
* `.env` — Environment configuration file for secret API keys.

---

### Installation & Setup

#### 1. Clone the Repository & Fetch Dependencies

Clone this repository and easily deploy all necessary libraries using the `requirements.txt` file:

```bash
git clone https://github.com/ToasterRooter/ai-recon-osint-agent.git
cd ai-recon-osint-agent

# Install all required libraries automatically
pip install -r requirements.txt

```

#### 2. Environment Configuration

Open a `.env` file in the root directory of the project and populate it with your personal API credentials:

```env
OPENROUTER_KEY=your_openrouter_api_key_here
SHODAN_KEY=your_shodan_api_key_here
VIRUSTOTAL_KEY=your_virustotal_api_key_here
ABUSEIPDB_KEY=your_abuseipdb_api_key_here
LEAKIX_KEY=your_leakix_api_key_here

```

---

### Usage Instruction

Fire up the terminal script:

```bash
python main.py

```

#### Workflow Overview:

1. The terminal banner boots up, verifying the loading sequence of your security modules.
2. Provide a domain name or IP target at the console prompt: `recon (enter target ip/domain) > `.
3. The aggregator fetches structural data packets asynchronously across all endpoints.
4. You enter the interactive **Session Results Management Menu**:
* **Option 1:** Inspect the aggregate raw JSON tree and dump it into `reports/recon_[target]_raw_[timestamp].json`.
* **Option 2:** Instruct the AI Analyst to compile an expert security audit, written to `reports/recon_[target]_ai_report_[timestamp].txt`.
* **Option 3:** Jump into the continuous AI conversation room to interrogate the agent regarding specific vulnerabilities. Enter `back` to return to the option matrix.
