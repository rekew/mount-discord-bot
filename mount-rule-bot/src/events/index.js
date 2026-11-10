/**
 * Discord event registration.
 * @module events
 */

// Discord.js modules
import { Events } from 'discord.js';

// Local modules
import { handleClientReady } from './ready.js';
import { handleInteractionCreate } from './interactionCreate.js';
import { handleMessageCreate } from './messageCreate.js';

/**
 * Register every Discord event handler on the client.
 * @param {import('discord.js').Client} client Discord client to attach handlers to.
 * @returns {void}
 */
export function registerEvents(client) {
    client.once(Events.ClientReady, (readyClient) => handleClientReady(readyClient));
    client.on(Events.InteractionCreate, (interaction) =>
        handleInteractionCreate(interaction, client),
    );
    client.on(Events.MessageCreate, (message) => handleMessageCreate(message));
}
