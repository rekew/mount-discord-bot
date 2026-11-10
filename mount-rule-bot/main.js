import { ActionRowBuilder, Client, EmbedBuilder, GatewayIntentBits, StringSelectMenuBuilder, MessageFlags } from "discord.js"

import { RULE_TITLES, EMBED_COLOR } from './constants.js';

import dotenv from 'dotenv';

dotenv.config();

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent,
    ],
});

export const TOKEN = process.env.TOKEN
export const RULE_CHANNEL_ID = process.env.RULE_CHANNEL_ID
export const RULE_CHANNEL_SELECT_ID = process.env.RULE_CHANNEL_SELECT_ID
export const RULE_STORAGE_CHANNEL_ID = process.env.RULE_STORAGE_CHANNEL_ID
const STORAGE_MESSAGE_IDS = {
    general: process.env.RULE_GENERAL_MESSAGE_ID,
    chat: process.env.RULE_CHAT_MESSAGE_ID,
    voice: process.env.RULE_VOICE_MESSAGE_ID,
    ban: process.env.RULE_BAN_MESSAGE_ID,
};

const CACHE_TTL = 12 * 60 * 60 * 1000;
const embedCache = new Map();

async function getSectionEmbeds(key) {
    const cached = embedCache.get(key);
    if (cached && Date.now() < cached.expiresAt) return cached.embeds;

    const messageId = STORAGE_MESSAGE_IDS[key];
    if (!RULE_TITLES[key] || !messageId) {
        console.warn(`[select] unresolved key=${key} messageId=${messageId}`);
        return null;
    }

    const channel = await client.channels.fetch(RULE_STORAGE_CHANNEL_ID);
    const source = await channel.messages.fetch(messageId);
    if (!source.embeds.length) return [];

    embedCache.set(key, { embeds: source.embeds, expiresAt: Date.now() + CACHE_TTL });
    return source.embeds;
}

client.once('clientReady', async () => {
    console.log(`Logged in as ${client.user.tag}`)

    const channel = await client.channels.fetch(RULE_CHANNEL_ID)

    const recent = await channel.messages.fetch({ limit: 10 })

    const alreadySent = recent.some(
        (m) => m.author.id === client.user.id
    );

    if (alreadySent) {
        console.log("Message already exists, skipping...");
        return;
    }

    const embed = new EmbedBuilder()
        .setTitle('ПРАВИЛА ПРОЕКТА')
        .setDescription(
            `Мы поддерживаем свободное общение, сохраняя при этом чёткие границы допустимого поведения. Проект допускает жёсткий стиль общения, ненормативную лексику и соревновательный токсинг, если они не переходят в травлю, угрозы, преследование или другие недопустимые действия.

Сервер придерживается Правил сообщества Discord и условий использования платформы. Все участники обязаны соблюдать как внутренние правила проекта, так и официальные требования Discord.

Ознакомиться с официальными правилами можно здесь:
- [Правила сообщества Discord](https://discord.com/guidelines)
- [Условия использования Discord](https://discord.com/terms)

Выберите нужный раздел ниже, чтобы ознакомиться с подробной информацией.`
        )
        .setColor(EMBED_COLOR);

    const options = Object.entries(RULE_TITLES).map(([value, { label, description }]) => ({
        label,
        description,
        value,
    }));

    const menu = new StringSelectMenuBuilder()
        .setCustomId(RULE_CHANNEL_SELECT_ID)
        .setPlaceholder('Выбрать опцию')
        .addOptions(options)

    const row = new ActionRowBuilder().addComponents(menu);

    await channel.send({ embeds: [embed], components: [row] });
})

client.on('interactionCreate', async (interaction) => {
    if (!interaction.isStringSelectMenu()) return;
    if (interaction.customId !== RULE_CHANNEL_SELECT_ID) return;

    const key = interaction.values[0];
    const t0 = performance.now();

    try {
        const embeds = await getSectionEmbeds(key);

        if (embeds === null) {
            await interaction.reply({ content: 'Раздел не настроен.', flags: MessageFlags.Ephemeral });
            return;
        }

        if (!embeds.length) {
            await interaction.reply({ content: 'В разделе нет изображений.', flags: MessageFlags.Ephemeral });
            return;
        }

        await interaction.reply({ embeds, flags: MessageFlags.Ephemeral });

        console.log(`[select] key=${key} embeds=${embeds.length} total=${(performance.now() - t0).toFixed(0)}ms`);
    } catch (err) {
        console.error(`[select] failed key=${key}`, err);

        if (!interaction.replied && !interaction.deferred) {
            await interaction.reply({ content: 'Ошибка при загрузке правил.', flags: MessageFlags.Ephemeral }).catch(() => { });
        }
    }
})

client.on('messageCreate', async (message) => {
    if (message.author.bot) return;

    if (message.content === "!ping") {
        message.reply('Pong!');
    }
});

client.login(TOKEN)