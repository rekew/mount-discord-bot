/**
 * Environment configuration for the Mount rules bot.
 * @module config
 */

// Node.js modules
import { fileURLToPath } from 'node:url';

// Third-party modules
import dotenv from 'dotenv';

dotenv.config({ path: fileURLToPath(new URL('../.env', import.meta.url)) });

/** Discord bot token. */
export const TOKEN = process.env.TOKEN;

/** Channel where the rules panel is published. */
export const RULE_CHANNEL_ID = process.env.RULE_CHANNEL_ID;

/** Custom id of the rules section select menu. */
export const RULE_CHANNEL_SELECT_ID = process.env.RULE_CHANNEL_SELECT_ID;

/** Channel that stores the rendered rule section messages. */
export const RULE_STORAGE_CHANNEL_ID = process.env.RULE_STORAGE_CHANNEL_ID;

/** Storage message id per rule section key. */
export const RULE_STORAGE_MESSAGE_IDS = {
    general: process.env.RULE_GENERAL_MESSAGE_ID,
    chat: process.env.RULE_CHAT_MESSAGE_ID,
    voice: process.env.RULE_VOICE_MESSAGE_ID,
    ban: process.env.RULE_BAN_MESSAGE_ID,
};

/** Environment variables required by the bot runtime. */
export const BOT_ENV_KEYS = [
    'TOKEN',
    'RULE_STORAGE_CHANNEL_ID',
    'RULE_CHANNEL_ID',
    'RULE_CHANNEL_SELECT_ID',
];

/** Environment variables required by the section publishing script. */
export const INIT_ENV_KEYS = ['TOKEN', 'RULE_STORAGE_CHANNEL_ID'];

/**
 * Ensure that every required environment variable is present.
 * @param {string[]} keys Environment variable names to validate.
 * @returns {void}
 * @throws {Error} When one or more variables are missing.
 */
export function requireConfig(keys) {
    const missing = keys.filter((key) => !process.env[key]);

    if (missing.length > 0) {
        throw new Error(`Missing required environment variables: ${missing.join(', ')}`);
    }
}
