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

export const RULE_IMAGES = {
    general: ['1.1.png', '1.2.png', '1.3.png', '1.4.png', '1.5.png', '1.6.png', '1.7.png', '1.8.png', '1.9.png'],
    chat: ['2.1.png', '2.2.png', '2.3.png'],
    voice: ['3.1.png', '3.2.png'],
    ban: ['4.1.png', '4.2.png', '4.3.png'],
};

export const SECTION_TITLES = Object.fromEntries(
    Object.values(RULE_TITLES).map(({ section, label }) => [String(section), label])
);

export const EMBED_COLOR = '#293636'
