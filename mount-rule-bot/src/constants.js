/**
 * Static domain constants for the rules bot.
 * @module constants
 */

/** Metadata for each rule section shown in the select menu. */
export const RULE_TITLES = {
    general: {
        section: 1,
        label: 'Общие Правила',
        description: 'Правила 1.1–1.9: основы поведения на сервере',
    },
    chat: {
        section: 2,
        label: 'Правила Чата',
        description: 'Правила 2.1–2.3: общение в текстовых каналах',
    },
    voice: {
        section: 3,
        label: 'Правила Войса',
        description: 'Правила 3.1–3.2: поведение в голосовых каналах',
    },
    ban: {
        section: 4,
        label: 'При Получение Бана',
        description: 'Правила 4.1–4.3: что делать при получении бана',
    },
};

/** Section number mapped to its human-readable title. */
export const SECTION_TITLES = Object.fromEntries(
    Object.values(RULE_TITLES).map(({ section, label }) => [String(section), label]),
);

/** Accent color used by every rule embed. */
export const EMBED_COLOR = '#293636';

/** How long fetched section embeds stay cached (12 hours). */
export const EMBED_CACHE_TTL_MS = 12 * 60 * 60 * 1000;

/** Number of recent panel-channel messages scanned for an existing panel. */
export const PANEL_SCAN_LIMIT = 10;
