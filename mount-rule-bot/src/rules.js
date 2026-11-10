/**
 * Rule section storage lookups with a TTL cache.
 * @module rules
 */

// Local modules
import { RULE_STORAGE_CHANNEL_ID, RULE_STORAGE_MESSAGE_IDS } from './config.js';
import { EMBED_CACHE_TTL_MS, RULE_TITLES } from './constants.js';

/** Cached embeds keyed by section key. */
const embedCache = new Map();

/**
 * Fetch the embeds for a rule section from the storage channel.
 * Returns `null` when the section is not configured and an empty array when
 * the storage message contains no embeds.
 * @param {import('discord.js').Client} client Discord client used to fetch messages.
 * @param {string} key Rule section key.
 * @returns {Promise<import('discord.js').Embed[] | null>} Section embeds or a status marker.
 */
export async function getSectionEmbeds(client, key) {
    const cached = embedCache.get(key);

    if (cached && Date.now() < cached.expiresAt) {
        return cached.embeds;
    }

    const messageId = RULE_STORAGE_MESSAGE_IDS[key];

    if (!RULE_TITLES[key] || !messageId) {
        console.warn(`[rules] unresolved key=${key} messageId=${messageId}`);
        return null;
    }

    const channel = await client.channels.fetch(RULE_STORAGE_CHANNEL_ID);
    const source = await channel.messages.fetch(messageId);

    if (!source.embeds.length) {
        return [];
    }

    embedCache.set(key, {
        embeds: source.embeds,
        expiresAt: Date.now() + EMBED_CACHE_TTL_MS,
    });

    return source.embeds;
}
