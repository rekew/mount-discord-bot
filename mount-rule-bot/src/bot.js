/**
 * Bot startup for the Mount rules bot.
 * @module bot
 */

// Local modules
import { BOT_ENV_KEYS, TOKEN, requireConfig } from './config.js';
import { createClient } from './client.js';
import { registerEvents } from './events/index.js';

/**
 * Validate configuration, register event handlers and log the bot in.
 * @returns {Promise<void>}
 */
export async function startBot() {
    requireConfig(BOT_ENV_KEYS);

    const client = createClient();
    registerEvents(client);

    try {
        await client.login(TOKEN);
    } catch (error) {
        console.error('[bot] login failed', error);
        client.destroy();
        process.exitCode = 1;
    }
}
