import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

BOT_TOKEN = os.getenv('TG_BOT_TOKEN', '').strip()

# Прокси для обхода блокировки Telegram (актуально для РФ).
TG_PROXY = os.getenv('TG_PROXY', '').strip()

def _ids(raw: str):
    out = []
    if not raw:
        return out
    for part in raw.replace(';', ',').split(','):
        part = part.strip()
        if part.isdigit():
            out.append(int(part))
    return out

# Собираем админов из отдельных переменных TG_ADMIN_1, TG_ADMIN_2, ...
ADMIN_IDS = []

# Способ 1: Из отдельных переменных TG_ADMIN_1, TG_ADMIN_2, ...
for key, value in os.environ.items():
    if key.startswith('TG_ADMIN_') and key[9:].isdigit():  # key[9:] - номер после TG_ADMIN_
        try:
            admin_id = int(value.strip())
            if admin_id not in ADMIN_IDS:  # избегаем дублей
                ADMIN_IDS.append(admin_id)
        except (ValueError, AttributeError):
            pass

# Способ 2: Старый формат с запятой (для совместимости)
if not ADMIN_IDS:
    old_format = os.getenv('TG_ADMIN_IDS', '')
    if old_format:
        ADMIN_IDS = _ids(old_format)

# Сортируем для удобства
ADMIN_IDS.sort()

# Для отладки - выводим в лог
print(f"[CONFIG] Loaded {len(ADMIN_IDS)} admins: {ADMIN_IDS}")

EXPORT_CHAT_ID = os.getenv('EXPORT_CHAT_ID', '').strip()
EXPORT_INTERVAL_MIN = int(os.getenv('EXPORT_INTERVAL_MIN', '60') or '0')

DB = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'database': os.getenv('DB_DATABASE', 'metrostroi'),
    'user': os.getenv('DB_USERNAME', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
}