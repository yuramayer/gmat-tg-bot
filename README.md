# GMAT Бот

## Структура проекта

```text
bot_project/
│
├── app.py                 # Точка входа: инициализация бота и диспетчера
├── config.py              # Настройки: токен бота, URL БД, режимы логирования
│
├── db/
│   ├── base.py            # engine + sessionmaker (session_factory)
│   ├── models.py          # SQLAlchemy ORM-модели (User, MessageLog, etc)
│
├── repositories/
│   ├── base.py            # Базовый репозиторий с общими методами (add, delete, commit)
│   ├── user_repo.py       # UserRepository — CRUD для пользователей
│   ├── message_repo.py    # MessageRepository — CRUD для логов сообщений
│
├── services/
│   ├── user_service.py    # UserService — бизнес-логика вокруг пользователей (регистрация, бан, etc.)
│   ├── message_service.py # MessageService — сохранение истории сообщений, аналитика
│
├── middlewares/
│   ├── db_session.py      # DbSessionMiddleware: создаёт AsyncSession на каждый апдейт
│
├── routers/
│   ├── __init__.py        # Импорт и объединение всех роутеров
│   ├── start.py           # /start — регистрация пользователя, приветствие
│   ├── help.py            # /help — вывод подсказок
│   ├── echo.py            # fallback-хендлер (эхо или дефолтный ответ)
│
├── utils/
│   ├── logging.py         # Настройка логирования (JSON, stdout, etc.)
│   ├── validators.py      # Общие валидации, парсеры
│
└── tests/
    ├── test_repos.py      # unit-тесты репозиториев
    ├── test_services.py   # unit-тесты сервисов

```