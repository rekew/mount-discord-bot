import { readdirSync } from 'node:fs';
import { AttachmentBuilder, Client, EmbedBuilder, GatewayIntentBits } from 'discord.js';

import { EMBED_COLOR, SECTION_TITLES } from './constants.js';

import dotenv from 'dotenv';

dotenv.config();

const TOKEN = process.env.TOKEN;
const RULE_STORAGE_CHANNEL_ID = process.env.RULE_STORAGE_CHANNEL_ID;

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent,
    ],
});

const imagesBySection = readdirSync('./images').reduce((acc, name) => {
    const match = name.match(/^(\d+)\.(\d+)\.\w+$/);
    if (!match) return acc;

    const [, section, index] = match;
    if (!acc[section]) acc[section] = [];

    acc[section].push({ name, index: Number(index) });
    return acc;
}, {});

for (const section of Object.keys(imagesBySection)) {
    imagesBySection[section].sort((a, b) => a.index - b.index);
}

client.once('clientReady', async () => {
    console.log(`Logged in as ${client.user.tag}`);

    const channel = await client.channels.fetch(RULE_STORAGE_CHANNEL_ID);

    const sections = Object.keys(SECTION_TITLES).sort((a, b) => Number(a) - Number(b));

    for (const section of sections) {
        const images = imagesBySection[section];
        if (!images?.length) {
            console.warn(`section ${section} skipped: no images`);
            continue;
        }

        const files = images.map(({ name }) => new AttachmentBuilder(`./images/${name}`));

        const embeds = images.map(({ name }, i) => {
            const embed = new EmbedBuilder()
                .setColor(EMBED_COLOR)
                .setImage(`attachment://${name}`);

            if (i === 0) embed.setTitle(SECTION_TITLES[section]);

            if (i === images.length - 1) embed.setFooter({ text: 'Правила сервера Mount' });

            return embed;
        });

        const message = await channel.send({ embeds, files });
        console.log(`section ${section} messageId=${message.id}`);
    }

    client.destroy();
});

client.login(TOKEN);
