/**
 * Message event handler for simple text commands.
 * @module events/messageCreate
 */

// Local modules
import { PING_REPLY } from '../texts.js';

/**
 * Reply to the ping command.
 * @param {import('discord.js').Message} message Received message.
 * @returns {Promise<void>}
 */
export async function handleMessageCreate(message) {
    if (message.author.bot) {
        return;
    }

    if (message.content === '!ping') {
        await message.reply(PING_REPLY);
    }
}
