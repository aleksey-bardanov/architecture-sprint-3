# Команды для работы с приложением локально

## Виртуальное окружение 

- создание: `python3 -m venv .venv`
- активация: `source .venv/bin/activate`
- деактивация: `deactivate`

## Проверка работы сервиса

- поднятие сервиса локально: `uvicorn devices:app --host 0.0.0.0 --port 8180`
- проверка работы api: `localhost:8180/docs`
