### Hexlet tests and linter status:
[![Actions Status](https://github.com/lasnick7/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/lasnick7/python-project-83/actions)

## https://python-project-83-omjz.onrender.com/

Приложение на базе фреймворка Flask, построенное на MVC-архитектуре. Приложение проверяет доступность сайта, извлекает и анализирует ключевые HTML-элементы (title, h1, description), проверяет статус ответа сервера и позволяет сохранять историю проверок.

### Используемые технологии
|     Tools      | Version |
|:--------------:|:-------:|
|     Python     | ^3.13.0 |
|     Flask      | ^3.1.0  |
|     gunicorn   | ^23.0.0 |
| python-dotenv  | ^1.1.0  |
|     ruff       | ^0.11.4 |
| psycopg2-binary| ^2.9.10 |
| beautifulsoup4 | ^4.13.4 |
|     requests   | ^2.32.4 |
|     validators | ^0.35.0 |

### Установка и запуск

1. Установка зависимостей:
   
```bash
make install
```

2. Запуск dev-сервера

```bash
make dev
```

3. Линтер
   
```bash
 make lint
```

4. Сборка и запуск приложения:
   
```bash
make build
make start-server
```