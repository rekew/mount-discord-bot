/**
 * Publishing of the persistent rules panel.
 * @module panel
 */

// Local modules
import { RULE_CHANNEL_ID, RULE_CHANNEL_SELECT_ID } from './config.js';
import { PANEL_SCAN_LIMIT } from './constants.js';
import { buildRulesPanelEmbed, buildRulesPanelRow } from './embeds.js';

/**
 * Check whether a message already contains the rules panel select menu.
 * @param {import('discord.js').Message} message Message to inspect.
 * @param {string} selectId Custom id of the panel select menu.
 * @returns {boolean} `true` when the message contains the panel menu.
 */
function containsPanelSelect(message, selectId) {
    return message.components.some((row) =>
        row.components.some((component) => component.customId === selectId),
    );
}

/**
 * Publish the rules panel, unless an existing one is already present.
 * @param {import('discord.js').Client<true>} client Logged-in Discord client.
 * @returns {Promise<void>}
 */
export async function ensureRulesPanel(client) {
    const channel = await client.channels.fetch(RULE_CHANNEL_ID);
    const recent = await channel.messages.fetch({ limit: PANEL_SCAN_LIMIT });

    const alreadySent = recent.some(
        (message) =>
            message.author.id === client.user.id &&
            containsPanelSelect(message, RULE_CHANNEL_SELECT_ID),
    );

    if (alreadySent) {
        console.log('Rules panel already exists, skipping...');
        return;
    }

    await channel.send({
        embeds: [buildRulesPanelEmbed()],
        components: [buildRulesPanelRow(RULE_CHANNEL_SELECT_ID)],
    });
}
