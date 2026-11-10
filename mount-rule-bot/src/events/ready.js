/**
 * Client ready event handler.
 * @module events/ready
 */

// Local modules
import { ensureRulesPanel } from '../panel.js';

/**
 * Publish the rules panel once the client is ready.
 * @param {import('discord.js').Client<true>} client Logged-in Discord client.
 * @returns {Promise<void>}
 */
export async function handleClientReady(client) {
    console.log(`Logged in as ${client.user.tag}`);
    await ensureRulesPanel(client);
}
