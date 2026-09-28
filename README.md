# RollK20Bot

Telegram-бот для бросков кубов в настольных играх.
Поддерживает форматы `d20`, `3k4`, `2d6+2`, `1d20-1`.

## Возможности

- Бросок любого количества кубов с любым числом граней
- Модификатор к результату (`+N` / `-N`)
- Латинские `d`/`D` и русские `k`/`K` — взаимозаменяемы
- Ограничения: 1–100 кубов, 2–1000 граней

## Команды

| Команда | Описание |
|---|---|
| `/start` | Приветствие и краткая справка |
| `/roll 3k4+2` | Бросок 3 кубов с 4 гранями и модификатором +2 |
| `/roll d20` | Бросок одного d20 |
| `/roll 2d6-1` | Бросок 2d6 с модификатором −1 |

## Установка

### 1. Клонировать репозиторий

```bash
git clone https://github.com/твой_ник/rollk20bot.git
cd rollk20bot
```

### 2. Создать виртуальное окружение

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Получить токен бота

Напиши [@BotFather](https://t.me/BotFather) в Telegram, создай бота командой `/newbot`, скопируй токен.

### 5. Настроить переменные окружения

```bash
cp .env.example .env
```

Открой `.env` и вставь свой токен:

```env
BOT_TOKEN=123456:ABC-DEF...
```

### 6. Запустить

```bash
python rollk20bot.py
```

## Стек

- Python 3.10+
- [aiogram 3.x](https://docs.aiogram.dev/) — фреймворк для Telegram Bot API
- [python-dotenv](https://github.com/theskumar/python-dotenv) — загрузка `.env`

## Лицензия

MIT 
