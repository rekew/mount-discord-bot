/**
 * Publish rendered rule sections to the storage channel.
 * @module scripts/init
 */

// Node.js modules
import { readdirSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

// Discord.js modules
import { AttachmentBuilder, Events } from 'discord.js';

// Local modules
import { createClient } from '../src/client.js';
import { INIT_ENV_KEYS, RULE_STORAGE_CHANNEL_ID, TOKEN, requireConfig } from '../src/config.js';
import { SECTION_TITLES } from '../src/constants.js';
import { buildSectionEmbeds } from '../src/embeds.js';

/** Absolute path to the optimized rule images. */
const IMAGES_DIR = fileURLToPath(new URL('../images/', import.meta.url));

/**
 * Group image file names by section number, sorted by rule index.
 * @returns {Record<string, string[]>} Section number mapped to ordered file names.
 */
function collectImagesBySection() {
    const grouped = readdirSync(IMAGES_DIR).reduce((sections, name) => {
        const match = name.match(/^(\d+)\.(\d+)\.\w+$/);

        if (!match) {
            return sections;
        }

        const [, section, index] = match;
        sections[section] ??= [];
        sections[section].push({ name, index: Number(index) });
        return sections;
    }, {});

    return Object.fromEntries(
        Object.entries(grouped).map(([section, images]) => [
            section,
            images.sort((a, b) => a.index - b.index).map(({ name }) => name),
        ]),
    );
}

/**
 * Send one message per rule section to the storage channel.
 * @param {import('discord.js').Client} client Logged-in Discord client.
 * @returns {Promise<void>}
 */
async function publishSections(client) {
    const channel = await client.channels.fetch(RULE_STORAGE_CHANNEL_ID);
    const imagesBySection = collectImagesBySection();
    const sections = Object.keys(SECTION_TITLES).sort((a, b) => Number(a) - Number(b));

    for (const section of sections) {
        const imageNames = imagesBySection[section];

        if (!imageNames?.length) {
            console.warn(`section ${section} skipped: no images`);
            continue;
        }

        const files = imageNames.map((name) => new AttachmentBuilder(path.join(IMAGES_DIR, name)));
        const embeds = buildSectionEmbeds(SECTION_TITLES[section], imageNames);

        const message = await channel.send({ embeds, files });
        console.log(`section ${section} messageId=${message.id}`);
    }
}

/**
 * Publish every rule section, then always disconnect the client.
 * @returns {Promise<void>}
 */
export async function runInit() {
    requireConfig(INIT_ENV_KEYS);

    const client = createClient();

    try {
        await client.login(TOKEN);
        await new Promise((resolve) => client.once(Events.ClientReady, resolve));
        await publishSections(client);
    } catch (error) {
        console.error('[init] failed', error);
        process.exitCode = 1;
    } finally {
        client.destroy();
    }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
    await runInit();
}
