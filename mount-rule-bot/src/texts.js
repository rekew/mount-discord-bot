/**
 * User-facing texts used across the rules bot.
 * @module texts
 */

/** Title of the rules panel embed. */
export const PANEL_TITLE = 'ПРАВИЛА ПРОЕКТА';

/** Description of the rules panel embed. */
export const PANEL_DESCRIPTION = `Мы поддерживаем свободное общение, сохраняя при этом чёткие границы допустимого поведения. Проект допускает жёсткий стиль общения, ненормативную лексику и соревновательный токсинг, если они не переходят в травлю, угрозы, преследование или другие недопустимые действия.

Сервер придерживается Правил сообщества Discord и условий использования платформы. Все участники обязаны соблюдать как внутренние правила проекта, так и официальные требования Discord.

Ознакомиться с официальными правилами можно здесь:
- [Правила сообщества Discord](https://discord.com/guidelines)
- [Условия использования Discord](https://discord.com/terms)

Выберите нужный раздел ниже, чтобы ознакомиться с подробной информацией.`;

/** Placeholder shown in the sections select menu. */
export const PANEL_SELECT_PLACEHOLDER = 'Выбрать опцию';

/** Reply when a section has no storage message configured. */
export const SECTION_NOT_CONFIGURED = 'Раздел не настроен.';

/** Reply when the configured storage message has no embeds. */
export const SECTION_EMPTY = 'В разделе нет изображений.';

/** Reply when loading a section fails unexpectedly. */
export const RULES_LOAD_ERROR = 'Ошибка при загрузке правил.';

/** Reply to the ping command. */
export const PING_REPLY = 'Pong!';

/** Footer shown on the last embed of each rule section. */
export const SECTION_FOOTER = 'Правила сервера Mount';
