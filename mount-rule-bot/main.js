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
        .setTitle('Выберите опцию')
        .setDescription('Выберите что-то снизу из меню')
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
        const messageId = STORAGE_MESSAGE_IDS[key];
        if (!RULE_TITLES[key] || !messageId) {
            console.warn(`[select] unresolved key=${key} messageId=${messageId}`);
            await interaction.reply({ content: 'Раздел не настроен.', flags: MessageFlags.Ephemeral });
            return;
        }

        const channel = await client.channels.fetch(RULE_STORAGE_CHANNEL_ID);
        const source = await channel.messages.fetch(messageId);

        if (!source.embeds.length) {
            await interaction.reply({ content: 'В разделе нет изображений.', flags: MessageFlags.Ephemeral });
            return;
        }

        await interaction.reply({ embeds: source.embeds, flags: MessageFlags.Ephemeral });

        console.log(`[select] key=${key} embeds=${source.embeds.length} total=${(performance.now() - t0).toFixed(0)}ms`);
    } catch (err) {
        console.error(`[select] failed key=${key}`, err);

        if (!interaction.replied && !interaction.deferred) {
            await interaction.reply({ content: 'Ошибка при загрузке правил.', flags: MessageFlags.Ephemeral }).catch(() => {});
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