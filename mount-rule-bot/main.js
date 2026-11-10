import { ActionRowBuilder, Client, EmbedBuilder, GatewayIntentBits, StringSelectMenuBuilder, MessageFlags, AttachmentBuilder } from "discord.js"

import { RULE_CHOICES, RULE_TITLES, RULE_IMAGES, EMBED_COLOR } from './constants.js';

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

    let images = []

    switch (key) {
        case RULE_CHOICES.ads:
            images = RULE_IMAGES.ads;
            break;
        case RULE_CHOICES.security:
            images = RULE_IMAGES.security;
            break;
        case RULE_CHOICES.content:
            images = RULE_IMAGES.content;
            break;
        case RULE_CHOICES.behavior:
            images = RULE_IMAGES.behavior;
            break;
        case RULE_CHOICES.profile:
            images = RULE_IMAGES.profile;
            break;
        default:
            return;
    }

    const files = images.map((name) => new AttachmentBuilder(`./images/${name}`));

    const embeds = images.map((name, i) => {
        const embed = new EmbedBuilder()
            .setColor(EMBED_COLOR)
            .setImage(`attachment://${name}`);

        if (i === 0) embed.setTitle(RULE_TITLES[key].label);

        if (i === images.length - 1) embed.setFooter({ text: 'Правила сервера Mount' });

        return embed;
    });

    await interaction.reply({
        embeds,
        files,
        flags: MessageFlags.Ephemeral,
    });
})

client.on('messageCreate', async (message) => {
    if (message.author.bot) return;

    if (message.content === "!ping") {
        message.reply('Pong!');
    }
});

client.login(TOKEN)