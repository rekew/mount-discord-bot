"""User-facing texts, emoji and templates used across the bot."""

# Button emoji.
EMOJI_RENAME: str = "<:pentosquaresolid:1569757175952445651>"
EMOJI_KICK: str = "<:userslashsolid:1569758420662226954>"
EMOJI_LIMIT: str = "<:usergroupsolid:1569757661606584463>"
EMOJI_PRIVACY: str = "<:unlocksolid:1569758049478901780>"
EMOJI_MUTE: str = "<:microphoneslashsolid:1569758091451310121>"
EMOJI_TRANSFER: str = "<:crownsolid:1569758018684584046>"

# Errors shared by the interaction guards.
NOT_IN_VOICE: str = "❌ Сначала зайдите в свою голосовую комнату."
NOT_ROOM_OWNER: str = "❌ Вы не являетесь владельцем этой комнаты."
ROOM_NOT_FOUND: str = "❌ Комната больше не существует."
MEMBER_LEFT_VOICE: str = "❌ Участник больше не находится в голосовом канале."
MEMBER_LEFT_ROOM: str = "❌ Этот участник уже покинул вашу комнату."

# Rename modal.
RENAME_MODAL_TITLE: str = "Переименовать комнату"
RENAME_INPUT_LABEL: str = "Новое название комнаты"
RENAME_INPUT_PLACEHOLDER: str = "Введите название..."
RENAME_SUCCESS: str = "✅ Название комнаты изменено на **{name}**."

# Member limit modal.
LIMIT_MODAL_TITLE: str = "Изменить лимит участников"
LIMIT_INPUT_LABEL: str = "Количество участников (0 — без ограничений)"
LIMIT_INPUT_PLACEHOLDER: str = "Например: 5"
LIMIT_INVALID: str = "❌ Введите число от 0 до 99."
LIMIT_DISABLED: str = "✅ Лимит участников отключён."
LIMIT_SET: str = "✅ Лимит комнаты установлен: **{limit}**."

# Kick flow.
KICK_SELECT_PLACEHOLDER: str = "Выберите участника..."
KICK_PROMPT: str = "Выберите участника, которому нужно запретить вход в эту комнату:"
KICK_NO_MEMBERS: str = "В вашей комнате сейчас нет других участников."
KICK_SUCCESS: str = (
    "✅ **{name}** отключён от комнаты и больше не сможет подключиться к ней."
)

# Mute flow.
MUTE_SELECT_PLACEHOLDER: str = "Выберите участника..."
MUTE_PROMPT: str = "Выберите участника, которому нужно запретить говорить в этой комнате:"
MUTE_NO_MEMBERS: str = "В вашей комнате сейчас нет других участников."
MUTE_STATUS_MUTED: str = "Сейчас заглушён"
MUTE_STATUS_ACTIVE: str = "Сейчас может говорить"
MUTE_SUCCESS: str = "✅ **{name}** больше не может говорить в этой комнате."
UNMUTE_SUCCESS: str = "✅ **{name}** снова может говорить в этой комнате."
MUTE_REASON_TEMPLATE: str = "Участнику запрещено говорить в комнате {owner}"
UNMUTE_REASON_TEMPLATE: str = "Участнику снова разрешено говорить в комнате {owner}"

# Ownership transfer flow.
TRANSFER_SELECT_PLACEHOLDER: str = "Выберите нового владельца..."
TRANSFER_PROMPT: str = "Выберите участника, который станет новым владельцем комнаты:"
TRANSFER_NO_MEMBERS: str = "В вашей комнате сейчас нет других участников."
TRANSFER_SUCCESS: str = "✅ Комната передана **{name}**."

# Privacy toggle.
PRIVACY_OPENED: str = "🔓 Комната теперь открыта для всех."
PRIVACY_CLOSED: str = "🔒 Комната теперь приватная."

# Control panel embed.
PANEL_TITLE: str = "🎙️ Управление голосовой комнатой"
PANEL_DESCRIPTION: str = (
    "Зайдите в свою голосовую комнату, чтобы управлять ею.\n\n"
    f"{EMOJI_RENAME} **Переименовать** — изменить название комнаты.\n"
    f"{EMOJI_KICK} **Исключить участника** — отключить участника и запретить ему повторный вход.\n"
    f"{EMOJI_MUTE} **Замутить** — запретить участнику говорить в этой комнате.\n"
    f"{EMOJI_TRANSFER} **Передать комнату** — назначить нового владельца.\n"
    f"{EMOJI_LIMIT} **Лимит участников** — установить ограничение на количество участников.\n"
    f"{EMOJI_PRIVACY} **Приватность** — закрыть или открыть комнату.\n\n"
    "Команды управления доступны только владельцу комнаты."
)

# Temporary room creation.
ROOM_NAME_TEMPLATE: str = "Комната {name}"
ROOM_CREATE_REASON: str = "Создание временной голосовой комнаты"
ROOM_DELETE_REASON: str = "Временная голосовая комната пуста"
KICK_REASON_TEMPLATE: str = "Участник ограничен владельцем комнаты {owner}"
KICK_DISCONNECT_REASON: str = "Отключён владельцем голосовой комнаты"

# Clear command.
CLEAR_INVALID_AMOUNT: str = "❌ Please provide a number between 1 and 100."
CLEAR_SUCCESS: str = "✅ Deleted {amount} messages."
CLEAR_MISSING_PERMISSIONS: str = "❌ You need Manage Messages permission."
CLEAR_BAD_ARGUMENT: str = "❌ Please provide a valid number."
