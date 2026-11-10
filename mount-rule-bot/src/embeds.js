/**
 * Embed and component builders for the rules bot.
 * @module embeds
 */

// Discord.js modules
import { ActionRowBuilder, EmbedBuilder, StringSelectMenuBuilder } from 'discord.js';

// Local modules
import { EMBED_COLOR, RULE_TITLES } from './constants.js';
import {
    PANEL_DESCRIPTION,
    PANEL_SELECT_PLACEHOLDER,
    PANEL_TITLE,
    SECTION_FOOTER,
} from './texts.js';

/**
 * Build the main rules panel embed.
 * @returns {EmbedBuilder} Configured panel embed.
 */
export function buildRulesPanelEmbed() {
    return new EmbedBuilder()
        .setTitle(PANEL_TITLE)
        .setDescription(PANEL_DESCRIPTION)
        .setColor(EMBED_COLOR);
}

/**
 * Build the section select menu row for the rules panel.
 * @param {string} selectId Custom id of the select menu.
 * @returns {ActionRowBuilder} Row containing the section select menu.
 */
export function buildRulesPanelRow(selectId) {
    const options = Object.entries(RULE_TITLES).map(([value, { label, description }]) => ({
        label,
        description,
        value,
    }));

    const menu = new StringSelectMenuBuilder()
        .setCustomId(selectId)
        .setPlaceholder(PANEL_SELECT_PLACEHOLDER)
        .addOptions(options);

    return new ActionRowBuilder().addComponents(menu);
}

/**
 * Build embeds for a single rule section.
 * @param {string} title Section title applied to the first embed.
 * @param {string[]} imageNames Attachment file names in display order.
 * @returns {EmbedBuilder[]} Embeds referencing the section images.
 */
export function buildSectionEmbeds(title, imageNames) {
    return imageNames.map((name, index) => {
        const embed = new EmbedBuilder().setColor(EMBED_COLOR).setImage(`attachment://${name}`);

        if (index === 0) {
            embed.setTitle(title);
        }

        if (index === imageNames.length - 1) {
            embed.setFooter({ text: SECTION_FOOTER });
        }

        return embed;
    });
}
