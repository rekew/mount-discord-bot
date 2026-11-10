/**
 * Shared Discord client factory.
 * @module client
 */

// Discord.js modules
import { Client, GatewayIntentBits } from 'discord.js';

/** Intents required by every entrypoint of the bot. */
const INTENTS = [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
];

/**
 * Create a Discord client with the intents required by the rules bot.
 * @returns {Client} A configured, not-yet-logged-in Discord client.
 */
export function createClient() {
    return new Client({ intents: INTENTS });
}
