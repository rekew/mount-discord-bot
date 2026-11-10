# Mount Bot

Два независимых Discord-бота для проекта Mount:

- **mount-rule-bot** — публикует панель правил с разделами и картинками, реагирует на выбор раздела в меню.
- **mount-voice-bot** — создаёт временные голосовые комнаты и управляет ими через панель с кнопками.

Оба сервиса запускаются через Docker Compose.

## Структура репозитория

```
.
├── docker-compose.yml
├── mount-rule-bot/
│   ├── main.js
│   ├── src/            # логика бота, события, тексты, embeds
│   ├── scripts/        # init.js и optimize-images.js
│   ├── images/         # оптимизированные WebP-картинки правил
│   ├── Dockerfile
│   └── .env.example
└── mount-voice-bot/
    ├── main.py
    ├── bot/            # клиент, команды, события, UI, состояние комнат
    ├── Dockerfile
    └── .env.example
```

## Требования

- [Docker](https://docs.docker.com/get-docker/)
- Docker Compose v2
- Приложение Discord с включёнными нужными intents (см. ниже)

Для локального запуска без Docker дополнительно нужны Node.js 20+, pnpm 11.8+ и Python 3.12+.

## Настройка окружения

Скопируйте шаблоны и заполните значения:

```bash
cp mount-rule-bot/.env.example mount-rule-bot/.env
cp mount-voice-bot/.env.example mount-voice-bot/.env
```

### mount-rule-bot

| Переменная                 | Обязательна | Описание                                                        |
| -------------------------- | ----------- | --------------------------------------------------------------- |
| `TOKEN`                    | да          | Токен Discord-приложения бота правил.                           |
| `RULE_CHANNEL_FOR_NON_VERIFIED_ID` | да          | Канал для панели правил участникам без верификации.             |
| `RULE_CHANNEL_FOR_VERIFIED`        | да          | Канал для панели правил верифицированным участникам.             |
| `RULE_CHANNEL_SELECT_ID`   | да          | Custom id меню выбора раздела (например, `rule_select_component`). |
| `RULE_STORAGE_CHANNEL_ID`  | да          | Канал, где хранятся сообщения с разделами правил.               |
| `RULE_GENERAL_MESSAGE_ID`  | нет         | ID сообщения раздела «Общие».                                   |
| `RULE_CHAT_MESSAGE_ID`     | нет         | ID сообщения раздела «Чат».                                     |
| `RULE_VOICE_MESSAGE_ID`    | нет         | ID сообщения раздела «Голос».                                   |
| `RULE_BAN_MESSAGE_ID`      | нет         | ID сообщения раздела «Баны».                                    |

ID сообщений разделов появляются после запуска `rule-init` (см. ниже) и выводятся в лог.

### mount-voice-bot

| Переменная | Обязательна | Описание                       |
| ---------- | ----------- | ------------------------------ |
| `TOKEN`    | да          | Токен Discord-приложения для голосового бота. |

Каналы и категории для голосового бота заданы в `mount-voice-bot/bot/config.py`.

### Intents в Discord Developer Portal

Для обоих приложений включите:

- **Message Content Intent**
- **Server Members Intent**
- **Voice States Intent** (для голосового бота)

## Запуск

Собрать образы и запустить оба бота:

```bash
docker compose up -d --build
```

Проверить статус и логи:

```bash
docker compose ps
docker compose logs -f
```

Остановить:

```bash
docker compose down
```

## Публикация разделов правил

Скрипт `init` отправляет сообщения с разделами правил в `RULE_STORAGE_CHANNEL_ID`. Его нужно запускать после изменения картинок или структуры разделов.

```bash
docker compose --profile tools build rule-init
docker compose --profile tools run --rm rule-init
```

В логе будут строки вида `section 1 messageId=...`. Перенесите полученные ID в `mount-rule-bot/.env` и перезапустите бота правил:

```bash
docker compose restart rule-bot
```

## Локальный запуск без Docker

### Бот правил

```bash
cd mount-rule-bot
pnpm install
pnpm start        # запуск бота
pnpm run init     # публикация разделов правил
```

Проверки качества кода:

```bash
pnpm lint
pnpm format:check
```

Оптимизация картинок (требуется установленный `cwebp` из пакета `webp`):

```bash
pnpm run optimize-images
```

### Голосовой бот

```bash
cd mount-voice-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Безопасность

- Файлы `.env` содержат токены и не должны попадать в git — они уже добавлены в `.gitignore`.
- Никогда не прикладывайте реальные токены к issue, pull request или скриншотам.
- При подозрении на утечку перевыпустите токен в Discord Developer Portal (Bot → Reset Token).

## Диагностика

| Проблема                                        | Решение                                                                 |
| ----------------------------------------------- | ----------------------------------------------------------------------- |
| `Missing required environment variables: ...`   | Заполните переменные в соответствующем `.env` и перезапустите сервис.   |
| Бот запускается, но не видит сообщения/участников | Включите нужные intents в Discord Developer Portal.                   |
| `Раздел не настроен` в панели правил            | Запустите `rule-init`, перенесите `RULE_*_MESSAGE_ID` в `.env`, перезапустите. |
| `docker compose` не находит `.env`              | Скопируйте `.env.example` в `.env` для каждого бота.                    |
