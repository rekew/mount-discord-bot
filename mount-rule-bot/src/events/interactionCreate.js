/**
 * Interaction event handler for the rules panel.
 * @module events/interactionCreate
 */

// Discord.js modules
import { MessageFlags } from 'discord.js';

// Local modules
import { RULE_CHANNEL_SELECT_ID } from '../config.js';
import { getSectionEmbeds } from '../rules.js';
import { RULES_LOAD_ERROR, SECTION_EMPTY, SECTION_NOT_CONFIGURED } from '../texts.js';

/**
 * Reply to rule section selections from the panel.
 * @param {import('discord.js').Interaction} interaction Received interaction.
 * @param {import('discord.js').Client} client Discord client used for lookups.
 * @returns {Promise<void>}
 */
export async function handleInteractionCreate(interaction, client) {
    if (!interaction.isStringSelectMenu()) {
        return;
    }

    if (interaction.customId !== RULE_CHANNEL_SELECT_ID) {
        return;
    }

    const key = interaction.values[0];
    const startedAt = performance.now();

    try {
        const embeds = await getSectionEmbeds(client, key);

        if (embeds === null) {
            await interaction.reply({
                content: SECTION_NOT_CONFIGURED,
                flags: MessageFlags.Ephemeral,
            });
            return;
        }

        if (!embeds.length) {
            await interaction.reply({
                content: SECTION_EMPTY,
                flags: MessageFlags.Ephemeral,
            });
            return;
        }

        await interaction.reply({ embeds, flags: MessageFlags.Ephemeral });

        const elapsed = (performance.now() - startedAt).toFixed(0);
        console.log(`[select] key=${key} embeds=${embeds.length} total=${elapsed}ms`);
    } catch (error) {
        console.error(`[select] failed key=${key}`, error);

        if (!interaction.replied && !interaction.deferred) {
            await interaction
                .reply({ content: RULES_LOAD_ERROR, flags: MessageFlags.Ephemeral })
                .catch(() => {});
        }
    }
}
